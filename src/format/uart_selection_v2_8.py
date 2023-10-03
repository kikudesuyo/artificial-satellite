import time

from util import shutdown
from flow.analysis import analysis_flow
from flow.downlink import get_downlink_data
from flow.shooting import shooting_flow
from flow.split import split_flow
from format.format import send_data, send_CMD, run, get_data_from_format, print_0xdata, FORMAT_ADRS_SENDER
from helper.status_operation import handle_based_on_previous_status, is_equal_command
from eps_line import set_eps_callback, input_from_eps, request_shutdown
from gpio_setting import set_gpio_line
from constant.format import GS_ADDR, CW_ADDR, EPS_ADDR, MC_ADDR, FORMAT_CMD
from constant.eps_relation import SAFE
from constant.command_list import (ACK_RPI_GS_SPLIT, CMD_RPI_CW_RESET, CMD_RPI_EPS_POWER_CHECK,
  CMD_RPI_MC_DOWNLINK, CMD_RPI_MC_DATE, CMD_GS_RPI_SPLIT, CMD_GS_RPI_DOWNLINK, ACK_CW_RPI_RESET, 
  ACK_EPS_RPI_POWER_CHECK, CMD_MC_RPI_CW_DATA, ACK_MC_RPI_DOWNLINK, CMD_MC_RPI_DOWNLINK_FINISH,
  ACK_MC_RPI_DATE)

class UartSelection:
  def __init__(self):
    self.last_format_array = [0, 0, 0, 0, 0]
    self.downlink_count = 0
    self.downlink_flag = False
    self.downlink_data = get_downlink_data()

  def selection(self, format_array):
    sender = FORMAT_ADRS_SENDER(format_array)
    cmd    = format_array[FORMAT_CMD]

    if sender == GS_ADDR:
      if cmd == CMD_GS_RPI_SPLIT:
        send_CMD(GS_ADDR, ACK_RPI_GS_SPLIT)
        print("split")
        split_flow()
        print("split_finish")
        request_shutdown()
      elif cmd == CMD_GS_RPI_DOWNLINK: #ダウンリンク指示コマンド
        #output_uplink_data(format_array)    
        self.downlink_flag = True
        #renew_downlink_status()
        #output_raspi_status(OTHERS_COMPLETION)
        print("downlink first time")
      else :
        print("NO_CMD")

    elif sender == CW_ADDR:
      if cmd == ACK_CW_RPI_RESET:
        print("CW received reset.")
      else:
        print("NO_CMD")

    elif sender == EPS_ADDR:
      if cmd == ACK_EPS_RPI_POWER_CHECK:
        #撮影後に継続か？
        power = get_data_from_format(format_array)[0]
        if power == SAFE:
          print("analysis_start")
          analysis_flow()
          print("analysis finish")
        else:
          print("power is danger. shutdown preparation.")
        request_shutdown()
      else :
        print("NO_CMD")
        
    elif sender == MC_ADDR:
      if cmd == CMD_MC_RPI_CW_DATA:
        send_CMD(CW_ADDR, CMD_RPI_CW_RESET)
      elif cmd == ACK_MC_RPI_DOWNLINK:
        self.downlink_count = 0
        self.downlink_flag = False
        #ダウンリンクが成功したためdownlink_statusを更新する必要がある
        self.downlink_data = get_downlink_data()
      elif cmd == CMD_MC_RPI_DOWNLINK_FINISH:
          #ダウンリンクステータスの変更をする必要がある
          #送るデータがあるなら要求、ないならシャットダウン(ダウンリンクに関しては２回目以降)
        if self.downlink_data == []:
          print("通信終了のためシャットダウンします")
          #shutdown()
        else:
          self.downlink_flag = True
          print("donwnlik multiple times")
      elif cmd == CMD_MC_RPI_SHOOTING:
        #緯度が範囲内になったら撮影
        send_CMD(ACK_RPI_MC_SHOOTING)
        time_data = get_data_from_format(format_array)
        print(time_data)
        print("satellite reached a designed lattitude.")
        shooting_flow()
        print("shooting finish")
        send_CMD(EPS_ADDR, CMD_RPI_EPS_POWER_CHECK)
      elif cmd == ACK_MC_RPI_DATE:
        #予約コマンドから時刻データを取得後撮影
        time_data = get_data_from_format(format_array)
        print(time_data)
        shooting_flow(time_data)
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
      send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
    else:
      #handle_based_on_previous_status()
      print("previous_status")
      #解析を行うかどうかを確認する
      if  1==0:
        analysis_flow()
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
        print_0xdata(self.last_format_array)
        print("=======finsh_handle_CMD=======")
        print()
      time.sleep(0.0001)