import pickle

from downlink.shape_up import get_aurora_data, get_splited_data
from format.format import send_data as communication_main
from util import delete_files
from helper.file_operation import output_raspi_status
from format.format import FORMAT_CMD, FORMAT_DATA_SIZE, FORMAT_DATA_START
from constant import COM_ADDR, OTHERS_COMPLETION, DOWNLINK_INTERRUPTION
from constant import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, IMAGE_SEND_COMPLETE
#from format.YOTSUBA_CMD_RPI import ACK_COM_RPI_DOWNLINK_FINISH, ACK_RPI_COM_DOWNLINK_TIMEOUT
from downlink.shape_up import make_data_for_downlink
from util import generate_path

def is_uplink_data_correct(format_array):
  data_size = format_array[FORMAT_DATA_SIZE]
  uplink_data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
  amount_file = (data_size - 1) / 3
  try:
    if amount_file % 1 == 0:
      return True
    else:
      raise ValueError("uplink data are broken.")
  except:
    return False  

def output_uplink_data(format_array):
  if is_uplink_data_correct(format_array):
    data_size = format_array[FORMAT_DATA_SIZE]
    uplink_data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
    rough_amount_file = uplink_data[1:]
    #配列のサイズを求めて配列を予め用意しておく。
    designed_files = []
    for index in range(int(data_size/3)):
      file_number = rough_amount_file[index]*256+rough_amount_file[index+1]*16+rough_amount_file[index]
      designed_files.append(file_number)
    status_file = open(generate_path("/src/flow/downlink_status.txt"), "wb")
    pickle.dump(designed_files, status_file)
    status_file.close()

def input_uplink_data():
  status_file = open(generate_path("/src/flow/downlink_status.txt"), "rb")
  designed_files = pickle.load(status_file)
  status_file.close()
  return designed_files


def downlink_flow(format_array):
  output_raspi_status(DOWNLINK_INTERRUPTION)
  uplink_data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
  send_type = uplink_data[0]
  designed_files = input_uplink_data()
  if send_type == AURORA_DATA:
    sending_data = make_data_for_downlink("/data/aurora_data/*.txt")
  elif send_type == AURORA_IMG:
    sending_data = make_data_for_downlink("/data/aurora_img/" + designed_files[0] + ".txt")
  elif send_type == DESIGNED_AURORA_IMG:
    if designed_files[0] == 0:
      sending_data = make_data_for_downlink("/data/aurora_img/" + designed_files[1] + ".txt")
    else:
      sending_data = make_data_for_downlink("/data/aurora_img/" + designed_files[0] + ".txt")
  elif send_type == IMAGE_SEND_COMPLETE:
    delete_files("/data/aurora_img")
    sending_data = "消しました" #削除したことを伝えるデータを用意してダウンリンク→ダウンリンク終了
  return sending_data