from downlink.shape_up import get_aurora_data, get_splited_data
from format.uart_communication import send_command, receive_command

def downlink_flow():
  if "オーロラデータ送信":
    aurora_data = get_aurora_data("/data/aurora_data/*")
  elif "画像データ送信":
    aurora_img = get_splited_data("/data/aurora_img/*.txt")
  elif "画像データ番号指定":
    aurora_img = get_splited_data("/data/aurora_data/*.txt")
  
  