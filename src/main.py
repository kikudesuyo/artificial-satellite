from format.uart_communication import send_command, receive_command
from flow.analysis import analysis_flow
from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow
from util import shutdown, delete_files

def execute():
  command = receive_command()
  
  if command == "オーロラ撮影":
    shooting_flow()
    after_shooting = "撮影処理"
  elif command == "画像解析" or after_shooting == "撮影後継続可能":
    analysis_flow()
  elif command == "画像分割":
    delete_files("/data/aurora_img")
    split_flow()
  elif command == "ダウンリンク":
    downlink_flow()
    communication_main(sending_data)
    send_command("通信終了")
    delete_files("/data/aurora_data")
  shutdown()