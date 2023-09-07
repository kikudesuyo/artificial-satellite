import time
import glob

from util import shutdown, generate_path
from flow.analysis import analysis_flow
from flow.downlink import generate_downlink_data, output_uplink_data, renew_downlink_status
from flow.shooting import shooting_flow
from flow.split import split_flow
from format.format import send_CMD, send_data, from_micon, get_data_from_format, print_0xdata, FORMAT_ADRS_SENDER, FORMAT_CMD
from helper.status_operation import handle_based_on_previous_status, is_equal_command, does_not_background_communicate, does_not_main_communicate
from helper.file_operation import output_communication_status, output_raspi_status
from format.command_list import *
from constant import GS_ADDR, CW_ADDR, EPS_ADDR, MC_ADDR, SAFE, MAIN_COMMUNICATING, BACKGROUND_COMMUNICATING, NONE_COMMUNICATING, OTHERS_COMPLETION, DOWNLINK_INTERRUPTION

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

def send_downlink_data(downlink_data):
  count = 0
  try:
    while count < 5:
      send_data(MC_ADDR, CMD_RPI_MC_DOWNLINK, downlink_data)
      cmd_list = run()
      for format_array in cmd_list:
        sender = FORMAT_ADRS_SENDER(format_array)
        cmd = format_array[FORMAT_CMD]
        if sender == MC_ADDR & cmd == ACK_MC_RPI_DONWLINK:
          output_raspi_status(OTHERS_COMPLETION)
          break
      time.sleep(3)
      count += 1
    if count == 5:
      raise ConnectionError("通信失敗")
  except Exception as e:
    print(e)
    print("通信失敗のためシャットダウンします。")
    output_raspi_status(DOWNLINK_INTERRUPTION)
    #shutdown()


def selection(format_array):
  sender = FORMAT_ADRS_SENDER(format_array)
  cmd    = format_array[FORMAT_CMD]
  
  if sender == GS_ADDR:
    if cmd == CMD_GS_RPI_SHOOTING: #撮影要求予約コマンド
      print("request date")
      send_CMD(MC_ADDR, CMD_RPI_MC_DATE)
    elif cmd == CMD_GS_RPI_SPLIT:
      print("ACK_RPI_GS_SPLIT")
      send_CMD(GS_ADDR, ACK_RPI_GS_SPLIT)
      print("split")
      split_flow()
      print("split_finish")
      time.sleep(1)
      send_CMD(EPS_ADDR, CMD_RPI_EPS_SHUTDOWN)
    elif cmd == CMD_GS_RPI_DOWNLINK: #ダウンリンク指示コマンド
      output_uplink_data(format_array)
      downlink_data = generate_downlink_data()
      send_downlink_data(downlink_data)
      renew_downlink_status()
      output_raspi_status(OTHERS_COMPLETION)
      #ダウンリンクステータスの変更をする必要がある
      print("down")
    else:
      print("NO_CMD")

  elif sender == CW_ADDR:
    if cmd == ACK_CW_RPI_RESET:
      print("CW received reset.")

  elif sender == EPS_ADDR:
    if cmd == CMD_EPS_RPI_SHUTDOWN:
      print("power is danger. shut down rpi.")
      send_CMD(EPS_ADDR, ACK_RPI_EPS_SHUTDOWN)
      #shutdown()
      time.sleep(100)
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
      time.sleep(100)
    else :
      print("NO_CMD")
      
  elif sender == MC_ADDR:
    if cmd == CMD_MC_RPI_CW_DATA:
      send_CMD(CW_ADDR, CMD_RPI_CW_RESET)
    elif cmd == ACK_MC_RPI_DONWLINK:
      pass
    elif cmd == CMD_MC_RPI_DOWNLINK_FINISH:
      output_uplink_data(format_array)
      downlink_data = generate_downlink_data()
      send_downlink_data(downlink_data)
      renew_downlink_status()
      output_raspi_status(OTHERS_COMPLETION)
      #ダウンリンクステータスの変更をする必要がある
      #送るデータがあるなら要求、ないならシャットダウン(ダウンリンクに関しては２回目以降)
      if downlink_data == []:
        if glob.glob(generate_path("/data/aurora_data/*")) == []:
          send_CMD(MC_ADDR, ACK_RPI_MC_DOWNLINK_FINISH)
          print("通信終了のためシャットダウンします")
          #shutdown()
      else:
        send_downlink_data(downlink_data)
        renew_downlink_status()
        output_raspi_status(OTHERS_COMPLETION)
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
      time.sleep(100)
    
def main():
  #send_CMD(MC_ADDR,CMD_RPI_MC_POWER_ON)#起動完了
  handle_based_on_previous_status()
  try:
    last_format_array = None
    while True:
      i = 0
      while True:
        if does_not_background_communicate():#statusファイルの居場所を変更してもいいかも
          print("break!!")#ここの挙動をraspiで確認した方がいい。一つ上のwhile trueのループがどうまわるか
          break
        elif i < 5:#この回数も決めた方がいい。どの程度待ってエラーが起きていると判断するか
          print("sleep!")
          i += 1
        else:
          print("Error! Background communication does not end or communication_status is not correct!")
          output_communication_status(NONE_COMMUNICATING)#ここの例外処理の相談した方がいい、例外処理の方法そのものや、例外処理の回数などを相談する。bacgroundも注意
          break
        time.sleep(5) #ここの時間は要相談, また、この時命令を送り続けてもらうようにする必要あり
      output_communication_status(MAIN_COMMUNICATING)
      cmd_list = run()
      output_communication_status(NONE_COMMUNICATING)
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
      i=0
      while True:
        if does_not_main_communicate():
          print("break")
          break
        elif i < 5:
          print("sleep!")
          i += 1
        else:
          print("This is the error! Background communication does not end or communication_status is not correct!")
          output_communication_status(NONE_COMMUNICATING)#ここの例外処理を相談した方がいい。例外処理の方法そのものや、例外処理の回数を相談する。mainも注意
          break
        time.sleep(5) #ここの時間は要相談, また、この時命令を送り続けてもらうようにする必要あり
        output_communication_status(BACKGROUND_COMMUNICATING)
        cmd_list=run() #runを書き換えてもいいかも。引数↑で↓は最後に加える
        output_communication_status(NONE_COMMUNICATING)
        for format_array in cmd_list:
          interruption(format_array)
        time.sleep(30)
  except Exception as e:
    print(e)
    pass