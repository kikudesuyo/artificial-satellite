from format.uart_communication import send_command, receive_command
from flow.analysis import analysis_flow
from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow
from util import shutdown, delete_files

def execute():
  send_command("起動完了")
  command = receive_command()
  
  if command == "オーロラ撮影":
    after_shooting = shooting_flow()
  if command == "画像解析" or after_shooting == "解析継続":
    analysis_flow()
  elif command == "画像分割":
    delete_files("/data/aurora_img")
    split_flow()
  elif command == "ダウンリンク":
    downlink_flow()
    send_command("シャットダウン要求")
  

  shutdown()