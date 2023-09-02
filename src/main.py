from format.uart_communication import send_command, receive_command
from flow.analysis import analysis_flow
from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow

def execute():
  command = receive_command()
  
  if command == "オーロラ撮影":
    """撮影フローに従う"""
    shooting_flow()
    after_shooting = "撮影処理"
  elif command == "画像解析" or after_shooting == "撮影後継続可能":
    """解析フローに従う"""
    analysis_flow()
  elif command == "画像分割":
    delete_files("/data/aurora_img")
    convert_img_into_text("/img/downlink_img/compressed_img.jpg")
    split_text_string("/data/downlink_data.txt")
    send_command("分割終了")
  elif command == "ダウンリンク":
    downlink_command = receive_command(15)
    if downlink_command == "オーロラデータダウンリンク":
      sending_data = get_aurora_data("/data/aurora_data/*.txt")
    elif downlink_command == "画像分割ダウンリンク":
      #indexの指定をどうするかを考える(オーロラデータは行わない予定なのでそこに注意)
      sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(sending_data)
    send_command("通信終了")
    delete_files("/data/aurora_data")
  shutdown()