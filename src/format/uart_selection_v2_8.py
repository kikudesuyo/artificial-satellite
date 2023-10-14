import time

from flow.analysis import analysis_flow
from flow.downlink import get_downlink_data
from flow.shooting import shooting_flow
from shooting.time_relation import decrypt_to_satellite_time, is_continuing_shooting
from flow.split import split_flow
from format.format import send_data, send_CMD, run, get_data_from_format, FORMAT_ADRS_SENDER
from downlink.uplink_edition import write_uplink_data_to_status
from downlink.status_edition import renew_status_file, initialize_status, write_uplink_info, check_uplink_info
from helper.file_operation import output_raspi_status
from eps_line import set_eps_callback, input_from_eps, request_shutdown_flow
from gpio_setting import set_gpio_line
from constant.format import GS_ADDR, MC_ADDR, FORMAT_CMD
from constant.status import SHOOTING_COMPLETION, SHOOTING_INTERRUPTION, INITIAL_DOWNLINK
from constant.shooting import INITIAL_TIMESTAMP
from constant.command_list import (ACK_RPI_GS_SPLIT, CMD_RPI_MC_DOWNLINK,CMD_RPI_MC_DATE,
ACK_RPI_MC_CW_DATA, CMD_GS_RPI_SPLIT, CMD_GS_RPI_DOWNLINK, CMD_GS_RPI_ANALYSIS, CMD_GS_RPI_TASK_INFO,
CMD_MC_RPI_CW_DATA, ACK_MC_RPI_DOWNLINK, CMD_MC_RPI_DOWNLINK_FINISH, ACK_MC_RPI_DATE)

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

  def selection(self, format_array):
    sender = FORMAT_ADRS_SENDER(format_array)
    cmd    = format_array[FORMAT_CMD]

    if sender == GS_ADDR:
      if cmd == CMD_GS_RPI_SPLIT:
        send_CMD(GS_ADDR, ACK_RPI_GS_SPLIT)
        print("split")
        split_flow()
        print("split_finish")
        #request_shutdown_flow()
      elif cmd == CMD_GS_RPI_DOWNLINK: #ダウンリンク指示コマンド
        if len(format_array) > 2:
          self.downlink_status = get_data_from_format(format_array)[0]
          write_uplink_data_to_status(self.downlink_status, format_array)
          self.downlink_data = get_downlink_data(self.downlink_status)
          if self.downlink_data != None:
            self.downlink_flag = True
            print("downlink first time")
          else:
            print("downlink data is None")
      elif cmd == CMD_GS_RPI_ANALYSIS:
        print("analysis start")
        analysis_flow()
        print("analysis finish")
        print("request shutdown")
        request_shutdown_flow()

      elif cmd == CMD_GS_RPI_TASK_INFO:
        uplink_info = get_data_from_format(format_array)
        if len(uplink_info) == 13:
          uplink_info = get_data_from_format(format_array)
          write_uplink_info(uplink_info)
          self.uplink_info = uplink_info[:13]
          self.shooting_flag = self.uplink_info[0]
          shooting_start_time = decrypt_to_satellite_time(self.uplink_info[1:5])
          shooting_finish_time = shooting_start_time+self.uplink_info[5]
          #shooting_interval = self.uplink_info[6]
          self.analysis_flag = self.uplink_info[7]
          analysis_start_time = decrypt_to_satellite_time(self.uplink_info[8:12])
          analysis_finish_time = analysis_start_time+self.uplink_info[12]
          print(self.uplink_info)
          print("checked_status")

      else :
        print("NO_CMD")
        
    elif sender == MC_ADDR:
      if cmd == CMD_MC_RPI_CW_DATA:
        send_CMD(MC_ADDR, ACK_RPI_MC_CW_DATA)
      elif cmd == ACK_MC_RPI_DOWNLINK:
        mc_sequence = get_data_from_format(format_array)
        if len(mc_sequence) == 2:
          self.send_MC_count = 0
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
          if back_sequence[1] == 1:
            self.send_MC_count = 0
            if back_sequence[0] == self.downlink_sequence_num:
              renew_status_file(self.downlink_status)        
              self.downlink_data = get_downlink_data(self.downlink_status)
              self.downlink_sequence_num = (self.downlink_sequence_num+1) & 0xff
              print(self.downlink_sequence_num)
              self.send_MC_count = 0
              if  self.downlink_data != None:
                self.downlink_flag = True
                self.send_MC_time = 0
                print("donwnlik multiple times")
              else: #back_sequence_num[1]==0
                self.downlink_flag = False
                send_CMD(MC_ADDR, CMD_RPI_MC_DOWNLINK)
                self.send_MC_time = 0
                self.downlink_sequence_num = 0
                #ダウンリンクステータスの変更をする必要がある
                #送るデータがあるなら要求、ないならシャットダウン(ダウンリンクに関しては２回目以降)
                print("通信終了のためシャットダウンします")
                #request_shutdown_flow()
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
          
      elif cmd == ACK_MC_RPI_DATE:
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
    if len(self.uplink_info) == 13:
      for i in range(13):
        self.uplink_info[i] = int(self.uplink_info[i],16)
      self.shooting_flag = self.uplink_info[0]
      shooting_start_time = decrypt_to_satellite_time(self.uplink_info[1:5])
      shooting_finish_time = shooting_start_time+self.uplink_info[5]
      #shooting_interval = self.uplink_info[6]
      self.analysis_flag = self.uplink_info[7]
      analysis_start_time = decrypt_to_satellite_time(self.uplink_info[8:12])
      analysis_finish_time = analysis_start_time+self.uplink_info[12]
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


    while True:
      time_now = time.time()
      adjusted_time = self.satellite_time+time_now-self.last_get_MC_time
      cmd_list = run()
      #print(adjusted_time)
      #print(self.shooting_flag)
      #print(shooting_start_time)
      
      #print(self.downlink_count)
      for format_array in cmd_list:
        self.selection(format_array)
        self.last_format_array = format_array
      
      if self.downlink_flag:
        if time_now- self.send_MC_time >= 5:
          send_data(MC_ADDR, CMD_RPI_MC_DOWNLINK, [int(self.downlink_sequence_num)] + self.downlink_data)
          self.send_MC_time = time.time()
          self.downlink_count += 1

      elif self.date_request_flag:
        if time_now-self.send_MC_time >= 2:
          output_raspi_status(SHOOTING_INTERRUPTION)
          send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
          self.send_MC_time = time.time()
          self.send_MC_count += 1
      
      elif self.shooting_flag:
        if shooting_start_time<adjusted_time and shooting_finish_time>adjusted_time:
          if self.initial_timestamp == INITIAL_TIMESTAMP:
            self.initial_timestamp = self.satellite_time
          if is_continuing_shooting(self.initial_timestamp, self.satellite_time):
            shooting_flow(self.satellite_time)
            print("SHOOTING_FINISH")
            output_raspi_status(SHOOTING_COMPLETION)
        elif shooting_finish_time<adjusted_time:
            self.shooting_flag = False

      elif self.analysis_flag:
        if adjusted_time>analysis_start_time and  adjusted_time<analysis_finish_time:
          print("analysis start")
          analysis_flow()
          self.analysis_flag = False
          print("analysis finish")
          print("shut down")
          request_shutdown_flow()   

        elif analysis_finish_time<adjusted_time:
          self.analysis_flag = False
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

      time.sleep(1)