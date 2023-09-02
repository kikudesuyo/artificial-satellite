from downlink.shape_up import get_aurora_data, get_splited_data
from format.uart_communication import send_command, receive_command
from downlink.main import main as communication_main
from util import delete_files

def downlink_flow():
  if "オーロラデータ送信":
    sending_data = get_aurora_data("/data/aurora_data/*")
    communication_main(sending_data)
    delete_files("/data/aurora_data")
  elif "画像データ送信":
    sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(sending_data)
  elif "画像データ番号指定":
    sending_data = get_splited_data("/data/aurora_data/*.txt")
    communication_main(sending_data)
  send_command("通信終了")
  