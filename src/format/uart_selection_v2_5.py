import time

from util import shutdown
from flow.analysis import analysis_flow
#from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow
from format.format import send_CMD, from_micon, get_data_from_format, print_0xdata, FORMAT_ADRS_SENDER, FORMAT_CMD
from helper.status_operation import handle_based_on_previous_status, is_equal_command, does_front_handle
from format.command_list import *
from constant import GS_ADDR, CW_ADDR, EPS_ADDR, MC_ADDR, SAFE

def run():
  cmd_list=[]
  while True:
    format_array = from_micon()
    if format_array==0:
      if len(cmd_list) != 0:
        print("receive_data:",end="")
        for l in cmd_list:
          print_0xdata(l)
      break
    else:
      cmd_list.append(format_array)
  return cmd_list

def selection(format_array):
  sender = FORMAT_ADRS_SENDER(format_array)
  cmd    = format_array[FORMAT_CMD]
  
  if sender == GS_ADDR:
    if cmd == CMD_GS_RPI_SHOOTING: #撮影要求予約コマンド
      print("request date")
      send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
    elif cmd == CMD_GS_RPI_SPLIT:
      print("ACK_RPI_GS_SPLIT")
      send_CMD(MC_ADDR, ACK_RPI_GS_SPLIT)
      print("split")
      split_flow()
      print("split_finish")
      time.sleep(1)
      send_CMD(EPS_ADDR, CMD_RPI_EPS_SHUTDOWN)
    elif cmd == CMD_GS_RPI_DOWNLINK: #ダウンリンク指示コマンド
      send_CMD(ACK_RPI_GS_DONWLINK)
      print("down")
      send_CMD(MC_ADDR, CMD_RPI_MC_DOWNLINK)
    else :
      print("NO_CMD")

  elif sender == CW_ADDR:
    if cmd == ACK_CW_RPI_RESET:
      print("CW received reset.")

  elif sender == EPS_ADDR:
    if cmd == CMD_EPS_RPI_SHUTDOWN:
      print("power is danger. shut down rpi.")
      send_CMD(EPS_ADDR, ACK_RPI_EPS_SHUTDOWN)
      #shutdown()
    elif cmd == ACK_EPS_RPI_POWER_CHECK:
      #撮影後に継続か？
      power = get_data_from_format(format_array)[0]
      if power == SAFE:
        print("analysis_start")
        analysis_flow()
        print("analysis finish")
      else:
        pass
      send_CMD(EPS_ADDR, CMD_RPI_EPS_SHUTDOWN)
    elif cmd == ACK_EPS_RPI_SHUTDOWN:
      print("approved shutdown")
      #shutdown()
    else :
      print("NO_CMD")
      
  elif sender == MC_ADDR:
    if cmd == CMD_MC_RPI_CW_DATA:
      send_CMD(CW_ADDR, CMD_RPI_CW_RESET)
    elif cmd == ACK_MC_RPI_DONWLINK:
      pass
    elif cmd == CMD_MC_RPI_DOWNLINK_FINISH:
      send_CMD(MC_ADDR, ACK_RPI_MC_DOWNLINK_FINISH)
      #送るデータがあるなら要求、ないならシャットダウン(ダウンリンクに関しては２回目以降)
      if "まだデータある？":
        send_CMD(MC_ADDR, CMD_RPI_MC_DOWNLINK)
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

#バックグラウンドのシャットダウン用
def interruption(format_array):
  sender = FORMAT_ADRS_SENDER(format_array)
  cmd    = format_array[FORMAT_CMD]
  if sender == EPS_ADDR:
    if cmd == CMD_EPS_RPI_SHUTDOWN:
      print("background_shut_down")
      send_CMD(EPS_ADDR, ACK_RPI_EPS_SHUTDOWN)
      #shutdown()
    
def main():
  handle_based_on_previous_status()
  try:
    last_format_array = None
    while True:
      cmd_list=run()
      for format_array in cmd_list:
        if last_format_array == None:
          selection(format_array)
          last_format_array = format_array
        else:
          if is_equal_command(format_array, last_format_array):
            print("same command")
            continue
          else: 
            selection(format_array)
            last_format_array = format_array
  except Exception as e:
    print(e)
    pass

def background():
  try:
    while True:
      if does_front_handle():
        cmd_list = run()
        for format_array in cmd_list:
          try:
            interruption(format_array)
          except Exception as e:
            print(e)
            pass
      else:
        time.sleep(5)
  except Exception as e:
    print(e)
    pass