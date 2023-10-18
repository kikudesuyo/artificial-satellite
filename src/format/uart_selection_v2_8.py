import time

from flow.analysis import analysis_flow
from flow.downlink import get_downlink_data
from flow.shooting import shooting_flow
from shooting.time_relation import decrypt_to_satellite_time, is_continuing_shooting
from flow.split import split_flow
from format.format import send_data, send_CMD, run, get_data_from_format, FORMAT_ADRS_SENDER
from downlink.uplink_edition import write_uplink_data_to_status
from downlink.status_edition import renew_status_file, initialize_status, write_uplink_info, check_uplink_info
from helper.file_operation import read_file_contents, delete_files_smaller_than_threshold
from eps_line import set_eps_callback, request_shutdown_flow
from gpio_setting import set_gpio_line
from constant.format import GS_ADDR, MC_ADDR, FORMAT_CMD, CW_ADDR
from constant.status import INITIAL_DOWNLINK, AURORA_DATA, MERGED_AURORA_DATA_NUMBER
from constant.shooting import INITIAL_TIMESTAMP
from constant.command_list import (ACK_RPI_GS_SPLIT, CMD_RPI_MC_DOWNLINK,CMD_RPI_MC_DATE,
ACK_RPI_MC_CW_DATA, CMD_GS_RPI_SPLIT, CMD_GS_RPI_DOWNLINK, CMD_GS_RPI_ANALYSIS, CMD_GS_RPI_TASK_INFO,
CMD_MC_RPI_CW_DATA, ACK_MC_RPI_DOWNLINK, CMD_MC_RPI_DOWNLINK_FINISH, ACK_MC_RPI_DATE, ACK_RPI_MC_DOWNLINK_FINISH)

class UartSelection:
  def __init__(self):
    self.last_format_array = [0, 0, 0, 0, 0]
    self.send_MC_count = 0
    self.downlink_flag = False
    self.date_request_flag = True
    self.downlink_data = None
    self.initial_timestamp = INITIAL_TIMESTAMP
    self.downlink_status = INITIAL_DOWNLINK
    self.downlink_sequence_num = 0
    self.send_MC_time = 0
    self.satellite_time = 0
    self.last_get_MC_time = time.time()
    self.shooting_flag = False
    self.analysis_flag = False
    self.split_flag = False
    self.ACK_uplink_flag = False

  def selection(self, format_array):
    sender = FORMAT_ADRS_SENDER(format_array)
    cmd    = format_array[FORMAT_CMD]

    if sender == GS_ADDR:
      self.downlink_flag = True
      if cmd == CMD_GS_RPI_SPLIT:
        self.ACK_uplink_flag = True
        self.split_flag = True
        self.downlink_data = [ACK_RPI_GS_SPLIT]
        #request_shutdown_flow()
      elif cmd == CMD_GS_RPI_DOWNLINK: #ダウンリンク指示コマンド
        if len(format_array) > 2:
          self.downlink_status = get_data_from_format(format_array)[0]
          write_uplink_data_to_status(self.downlink_status, format_array)
          self.downlink_data = get_downlink_data(self.downlink_status)
          print(self.downlink_data)
          if len(self.downlink_data) != 0:
            print("downlink first time")
          else:
            self.downlink_flag = False
            self.downlink_status = INITIAL_DOWNLINK
            self.downlink_sequence_num = 0
            print("downlink data is None")
            self.ACK_uplink_flag = True
            self.downlink_data = [CMD_GS_RPI_DOWNLINK]

      elif cmd == CMD_GS_RPI_ANALYSIS:
        self.ACK_uplink_flag = True
        self.downlink_data = [CMD_GS_RPI_ANALYSIS]
        self.analysis_flag = True
        print("analysis start")
        analysis_times = get_data_from_format(format_array)[0]
        for _ in range(analysis_times):
          analysis_flow()
        print("analysis finish")
        print("request shutdown")
        request_shutdown_flow()

      elif cmd == CMD_GS_RPI_TASK_INFO:
        uplink_info = get_data_from_format(format_array)
        self.ACK_uplink_flag = True
        if len(uplink_info) >= 12:
          write_uplink_info(uplink_info)
          self.uplink_info = uplink_info
          self.shooting_flag = self.uplink_info[0]
          self.shooting_start_time = decrypt_to_satellite_time(self.uplink_info[1:5])
          self.shooting_finish_time = self.shooting_start_time+self.uplink_info[5]*60
          self.analysis_flag = self.uplink_info[6]
          self.analysis_start_time = decrypt_to_satellite_time(self.uplink_info[7:11])
          self.analysis_start_time = self.analysis_start_time+self.uplink_info[11]*60
          print(self.uplink_info)
          self.downlink_data = [CMD_GS_RPI_TASK_INFO]
          print("checked_status")
        else:
          print("can't recive uplink correct")
          self.downlink_data = [0x00]

      else :
        self.ACK_uplink_flag = True
        self.downlink_data = [0x00]
        print("NO_CMD")
        
    elif sender == MC_ADDR:
      if cmd == CMD_MC_RPI_CW_DATA:
        send_CMD(MC_ADDR, ACK_RPI_MC_CW_DATA)
      elif cmd == ACK_MC_RPI_DOWNLINK:
        mc_sequence = get_data_from_format(format_array)
        if len(mc_sequence) == 2:
          self.send_MC_count = 0
          self.send_MC_time = 0
          if mc_sequence[1] == 1:
            if mc_sequence[0] == self.downlink_sequence_num:
              self.downlink_flag = False
            else:
              print("collect_carry_downlink_data")
          else:
            print("not_allowed_downlink")
        else:
          print("uncollect_downlink_ACK_data")

      elif cmd == CMD_MC_RPI_DOWNLINK_FINISH:
        back_sequence = get_data_from_format(format_array)
        if len(back_sequence) == 2:
          self.send_MC_time = 0
          self.send_MC_count = 0
          if back_sequence[1] == 1:
            if back_sequence[0] == self.downlink_sequence_num:
              if self.ACK_uplink_flag:
                self.ACK_uplink_flag = False
                self.downlink_flag = False
                self.downlink_data = None
                print("ACK_UPLINK_FINISH")
              else:
                if self.downlink_status == AURORA_DATA:
                  initial_file_name = read_file_contents("/src/status/aurora_data.txt")
                  if initial_file_name != "":
                    delete_files_smaller_than_threshold(int(initial_file_name)+MERGED_AURORA_DATA_NUMBER)
                renew_status_file(self.downlink_status)        
                self.downlink_data = get_downlink_data(self.downlink_status)
                self.downlink_sequence_num = (self.downlink_sequence_num+1) & 0xff
                # print(self.downlink_sequence_num)
                self.send_MC_count = 0
                # print(self.downlink_data)
                if len(self.downlink_data) != 0:
                  self.downlink_flag = True
                  print("downlink multiple times")
                else:
                  self.downlink_flag = False
                  send_CMD(MC_ADDR, ACK_RPI_MC_DOWNLINK_FINISH)
                  self.downlink_sequence_num = 0
          else:
            self.downlink_flag = False
            send_CMD(MC_ADDR, ACK_RPI_MC_DOWNLINK_FINISH)
            self.downlink_sequence_num = 0
            #ダウンリンクステータスの変更をする必要がある
            #送るデータがあるなら要求、ないならシャットダウン(ダウンリンクに関しては２回目以降)
        else:
          print("faild_ack")
          """
      elif cmd == CMD_MC_RPI_SHOOTING:
        #緯度が範囲内になったら撮影
        send_CMD(ACK_RPI_MC_SHOOTING)
        mc_time_data = get_data_from_format(format_array)
        print(mc_time_data)
        print("satellite reached a designed lattitude.")
        shooting_flow()
        print("shooting finish")
        """
    elif sender == CW_ADDR:
      if cmd == 0x0c:
        #予約コマンドから時刻データを取得後撮影
        mc_time_data = get_data_from_format(format_array)
        if len(mc_time_data) == 4:
          self.send_MC_count = 0
          self.date_request_flag = False
          self.last_get_MC_time = time.time()
          self.satellite_time = decrypt_to_satellite_time(mc_time_data)

      else :
        print("NO_CMD")
    else:
      print("no address")

  def main(self):
    set_gpio_line()
    print("set up finished")
    # eps_input_status = input_from_eps()
    set_eps_callback()
    """
    0byte shooting
    1~4   shooting_start_time[w,h,m,s]
    5     shooting_duration
    6     shooting_interval 
    7     analysis   
    8~11  analysis_start_time
    12    analysis_duration
    """
    initialize_status()
    self.uplink_info = check_uplink_info()
    if len(self.uplink_info) == 12:
      for i in range(12):
        self.uplink_info[i] = int(self.uplink_info[i],16)
      self.shooting_flag = self.uplink_info[0]
      self.shooting_start_time = decrypt_to_satellite_time(self.uplink_info[1:5])
      self.shooting_finish_time = self.shooting_start_time+self.uplink_info[5]*60
      self.analysis_flag = self.uplink_info[6]
      self.analysis_start_time = decrypt_to_satellite_time(self.uplink_info[7:11])
      self.analysis_finish_time = self.analysis_start_time+self.uplink_info[11]*60
      #print(self.uplink_info)
      print("checked_status")
    else:
      print("No_uplink_data")   
    #解析を行うかどうかを確認する
    """
    if eps_input_status:
      print("shooting_from_EPS")
      output_raspi_status(SHOOTING_INTERRUPTION)
      send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
    else:
    """
    time_flag = 1
    no_task_flag = 1
    no_task_time = 0
    last_task_time = time.time()

    while True:
      time_now = time.time()
      adjusted_time = self.satellite_time+time_now-self.last_get_MC_time
      cmd_list = run()
      if time_flag:
        p_time = int(adjusted_time)
        print("adjusted_time")
        # print(adjusted_time)
        minute  = int(adjusted_time/60)
        second  = adjusted_time%60
        print(f"{minute}m{second}s")
        """
        print("last_task_time)
        print(last_task_time)
        print("no_task_time")
        print(no_task_time)
        """
        time_flag = 0
      if adjusted_time-p_time > 1:
        time_flag = 1
      for format_array in cmd_list:
        self.selection(format_array)
        self.last_format_array = format_array
      
      if self.downlink_flag or self.shooting_flag or self.analysis_flag or self.split_flag: 
        no_task_flag = 0
        last_task_time = time_now
      else:
        no_task_flag = 1

      if self.downlink_flag:
        if time_now-self.send_MC_time >= 5:
          send_data(MC_ADDR, CMD_RPI_MC_DOWNLINK, [int(self.downlink_sequence_num)] + self.downlink_data)
          self.send_MC_time = time.time()
          self.send_MC_count += 1
      elif self.date_request_flag:
        if time_now- self.send_MC_time >= 4:
          send_CMD(CW_ADDR, 0x0c)
          self.send_MC_time = time.time()
          self.send_MC_count += 1

      elif self.date_request_flag:
        if time_now-self.send_MC_time >= 2:
          send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
          self.send_MC_time = time.time()
          self.send_MC_count += 1
      
      elif self.shooting_flag:
        if self.shooting_start_time<adjusted_time and self.shooting_finish_time>adjusted_time:
          if self.initial_timestamp == INITIAL_TIMESTAMP:
            self.initial_timestamp = self.satellite_time
          if is_continuing_shooting(self.initial_timestamp, self.satellite_time):
            shooting_flow(self.satellite_time)
            print("SHOOTING_FINISH")
            if not(self.analysis_flag or self.split_flag):
              print("sut down")
              request_shutdown_flow()   
        elif self.shooting_finish_time<adjusted_time:
            self.shooting_flag = False

      elif self.analysis_flag:
        if adjusted_time>self.analysis_start_time and  adjusted_time<self.analysis_finish_time:
          print("analysis start")
          analysis_flow()
          print("analysis finish")
          if not(self.split_flag):
            print("shut down")
            request_shutdown_flow()   
        elif self.analysis_finish_time<adjusted_time:
          self.analysis_flag = False


      elif self.split_flag:
        print("split")
        split_flow()
        self.split_flag = False
        print("shut down")
        request_shutdown_flow()

      if self.send_MC_count == 10:
        if self.date_request_flag and self.downlink_flag:
          self.send_MC_count = 0
          self.downlink_sequence_num = 0
          self.downlink_flag = False
          self.date_request_flag = False
          self.send_MC_time = 0
          initialize_status()
          print("fail communication")
          print("shut down")
          request_shutdown_flow()
      if no_task_flag:
        # print(time_now)
        # print(last_task_time)
        no_task_time = time_now - last_task_time
        print(no_task_time)
        if no_task_time > 600:
          print("no_task_10min")
          request_shutdown_flow()

      time.sleep(0.000001)