import time

from flow.analysis import analysis_flow
from flow.downlink import get_downlink_data
from flow.shooting import shooting_flow
from shooting.time_relation import decrypt_to_satellite_time, is_continuing_shooting
from flow.split import split_flow
from format.format import send_data, send_CMD, run, get_data_from_format, print_0xdata, FORMAT_ADRS_SENDER
from helper.status_operation import handle_based_on_previous_status, is_equal_command
from helper.file_operation import output_raspi_status
from eps_line import set_eps_callback, input_from_eps, request_shutdown_flow
from gpio_setting import set_gpio_line
from constant.format import GS_ADDR, CW_ADDR, EPS_ADDR, MC_ADDR, FORMAT_CMD
from constant.status import SHOOTING_COMPLETION, SHOOTING_INTERRUPTION, DOWNLINK_INTERRUPTION
from constant.shooting import INITIAL_TIMESTAMP
from constant.command_list import (ACK_RPI_GS_SPLIT, CMD_RPI_EPS_POWER_CHECK, CMD_RPI_MC_DOWNLINK,
CMD_RPI_MC_DATE, ACK_RPI_MC_CW_DATA, CMD_GS_RPI_SPLIT, CMD_GS_RPI_DOWNLINK, CMD_GS_RPI_ANALYSIS,
ACK_CW_RPI_RESET, CMD_MC_RPI_CW_DATA, ACK_MC_RPI_DOWNLINK, CMD_MC_RPI_DOWNLINK_FINISH, ACK_MC_RPI_DATE)

class UartSelection:
  def __init__(self):
    self.last_format_array = [0, 0, 0, 0, 0]
    self.downlink_count = 0
    self.downlink_flag = False
    self.downlink_data = None
    self.initial_timestamp = INITIAL_TIMESTAMP

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
        output_raspi_status(DOWNLINK_INTERRUPTION)
        self.downlink_data = get_downlink_data()
        self.downlink_flag = True
        #renew_downlink_status()
        print("downlink first time")
      elif cmd == CMD_GS_RPI_ANALYSIS:
        analysis_flow()
      else :
        print("NO_CMD")

    elif sender == CW_ADDR:
      if cmd == ACK_CW_RPI_RESET:
        print("CW received reset.")
      else:
        print("NO_CMD")
        
    elif sender == MC_ADDR:
      if cmd == CMD_MC_RPI_CW_DATA:
        send_CMD(MC_ADDR, ACK_RPI_MC_CW_DATA)
      elif cmd == ACK_MC_RPI_DOWNLINK:
        self.downlink_count = 0
        self.downlink_flag = False
        #ダウンリンクが成功したためdownlink_statusを更新する必要がある
        #シーケンス番号をみてから更新するためここでは不適切。82行目以降で処理するべき
        self.downlink_data = get_downlink_data()
      elif cmd == CMD_MC_RPI_DOWNLINK_FINISH:
          #ダウンリンクステータスの変更をする必要がある
          #送るデータがあるなら要求、ないならシャットダウン(ダウンリンクに関しては２回目以降)
          #シーケンス番号を確認してself.downlink_data = get_downlink_data() を更新
        if self.downlink_data == []:
          print("通信終了のためシャットダウンします")
          #shutdown()
        else:
          self.downlink_flag = True
          print("donwnlik multiple times")
      elif cmd == CMD_MC_RPI_SHOOTING:
        #緯度が範囲内になったら撮影
        send_CMD(ACK_RPI_MC_SHOOTING)
        mc_time_data = get_data_from_format(format_array)
        print(mc_time_data)
        print("satellite reached a designed lattitude.")
        shooting_flow()
        print("shooting finish")
      elif cmd == ACK_MC_RPI_DATE:
        #予約コマンドから時刻データを取得後撮影          
        mc_time_data = get_data_from_format(format_array)
        satellite_time = decrypt_to_satellite_time(mc_time_data)
        if self.initial_timestamp == INITIAL_TIMESTAMP:
          self.initial_timestamp = satellite_time
        if is_continuing_shooting(self.initial_timestamp, satellite_time):
          shooting_flow(satellite_time)
          print("SHOOTING_FINISH")
          output_raspi_status(SHOOTING_COMPLETION)
        else:
          request_shutdown_flow()
        print("SHOOTING_FINISH")
        #解析継続可能かどうか尋ねる
        send_CMD(EPS_ADDR, CMD_RPI_EPS_POWER_CHECK)
      else :
        print("NO_CMD")
    else:
      print("no address")

  def main(self):
    set_gpio_line()
    print("set up finished")
    eps_input_status = input_from_eps()
    set_eps_callback()
    if eps_input_status:
      print("shooting_from_EPS")
      output_raspi_status(SHOOTING_INTERRUPTION)
      send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
    else:
      #handle_based_on_previous_status()
      print("previous_status")
      #解析を行うかどうかを確認する
    while True:
      print("========CMD_LIST========")
      cmd_list = run()
      print(self.downlink_count)
      print()
      print("======handle_CMD======")
      for format_array in cmd_list:
        if is_equal_command(format_array, self.last_format_array):
          print("same command")
          continue
        else: 
          self.selection(format_array)
          self.last_format_array = format_array
      if self.downlink_flag:
        send_data(MC_ADDR, CMD_RPI_MC_DOWNLINK, self.downlink_data)
        self.downlink_count += 1
        if self.downlink_count == 5:
          self.downlink_count = 0
          self.downlink_flag = False
          print("fail communication")
          print("shut down")
          request_shutdown_flow()
        print_0xdata(self.last_format_array)
        print("=======finsh_handle_CMD=======")
        print()
      time.sleep(0.0001)