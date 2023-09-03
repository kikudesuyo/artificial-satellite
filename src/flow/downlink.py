from downlink.shape_up import get_aurora_data, get_splited_data
from format.uart_communication import send_command, receive_command
#from downlink.main import main as communication_main
from format.format import send_data as communication_main
from util import delete_files
from constant import COM_ADDR
from YOTSUBA_CMD_RPI import ACK_COM_RPI_DOWNLINK_FINISH

def downlink_flow():
  if "オーロラデータ送信":
    sending_data = get_aurora_data("/data/aurora_data/*")
    communication_main(COM_ADDR, ACK_RPI_COM_DOWNLINK_SEND, sending_data) #CMDについては九工大で確認
    delete_files("/data/aurora_data")
  elif "画像データ送信":
    sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(COM_ADDR, ACK_RPI_COM_DOWNLINK_SEND, sending_data)
  elif "画像データ番号指定":
    sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(COM_ADDR, ACK_RPI_COM_DOWNLINK_SEND, sending_data)
  elif "画像データ送信完了":
    delete_files("/data/aurora_img")