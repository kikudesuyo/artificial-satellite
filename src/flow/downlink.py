from downlink.shape_up import get_aurora_data, get_splited_data
from format.format import send_data as communication_main
from util import delete_files
from helper.file_operation import output_raspi_status
from format.format import FORMAT_CMD, FORMAT_DATA_SIZE, FORMAT_DATA_START
from constant import COM_ADDR, OTHERS_COMPLETION, DOWNLINK_INTERRUPTION
from constant import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, IMAGE_SEND_COMPLETE
#from format.YOTSUBA_CMD_RPI import ACK_COM_RPI_DOWNLINK_FINISH, ACK_RPI_COM_DOWNLINK_TIMEOUT

def downlink_flow(format_array):
  output_raspi_status(DOWNLINK_INTERRUPTION)
  command = format_array[FORMAT_CMD]
  designed_number = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]

  if command == AURORA_DATA:
    sending_data = get_aurora_data("/data/aurora_data/*")
    communication_main(COM_ADDR, ACK_RPI_COM_DOWNLINK_SEND, sending_data) #CMDについては九工大で確認
  elif command == AURORA_IMG:
    sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(COM_ADDR, ACK_RPI_COM_DOWNLINK_SEND, sending_data)
  elif command == DESIGNED_AURORA_IMG:
    sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(COM_ADDR, ACK_RPI_COM_DOWNLINK_SEND, sending_data)
  elif command == IMAGE_SEND_COMPLETE:
    delete_files("/data/aurora_img")
  output_raspi_status(OTHERS_COMPLETION)