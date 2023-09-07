from downlink.shape_up import get_aurora_data, get_splited_data
from format.format import send_data as communication_main
from util import delete_files
from helper.file_operation import output_raspi_status
from format.format import FORMAT_CMD, FORMAT_DATA_SIZE, FORMAT_DATA_START
from constant import COM_ADDR, OTHERS_COMPLETION, DOWNLINK_INTERRUPTION
from constant import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, IMAGE_SEND_COMPLETE
#from format.YOTSUBA_CMD_RPI import ACK_COM_RPI_DOWNLINK_FINISH, ACK_RPI_COM_DOWNLINK_TIMEOUT
from downlink.shape_up import make_data_for_downlink
def downlink_flow(format_array):
  output_raspi_status(DOWNLINK_INTERRUPTION)
  format_data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
  send_type = format_data[0]
  file_number = format_data[1]*256+format_data[2]*16+format_data[3]
  if send_type == AURORA_DATA:
    sending_data = make_data_for_downlink("/data/aurora_data/*.txt")
  elif send_type == AURORA_IMG:
    sending_data = make_data_for_downlink("/data/aurora_img/*.txt")
  elif send_type == DESIGNED_AURORA_IMG:
    sending_data = make_data_for_downlink("/data/aurora_img/" + file_number + ".txt")
  elif send_type == IMAGE_SEND_COMPLETE:
    delete_files("/data/aurora_img")
  output_raspi_status(OTHERS_COMPLETION)
  return sending_data