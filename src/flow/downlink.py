import pickle
import glob

from util import delete_files
from format.format import FORMAT_CMD, FORMAT_DATA_SIZE, FORMAT_DATA_START
from constant import COM_ADDR, OTHERS_COMPLETION, DOWNLINK_INTERRUPTION
from constant import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, IMAGE_SEND_COMPLETE
from downlink.shape_up import make_data_for_downlink
from util import generate_path

def is_uplink_data_correct(format_array):
  data_size = format_array[FORMAT_DATA_SIZE]
  try:
    if data_size % 3 == 0:
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
    if len(designed_files) >= 2:
      designed_files.append(0)
    status_file = open(generate_path("/src/flow/downlink_status.txt"), "wb")
    pickle.dump(designed_files, status_file)
    status_file.close()

def get_uplink_data():
  status_file = open(generate_path("/src/flow/downlink_status.txt"), "rb")
  designed_files = pickle.load(status_file)
  status_file.close()
  return designed_files

def renew_downlink_status():
  status = get_uplink_data()
  if len(status) == 0:
    delete_files("送ったオーロラデータだけを削除")
  elif len(status) == 1:
    status[0] = status[0] + 1
  else:
    if status[1] == 0:
      print("ダウンリンク終了")
      pass
    else:
      del status[0]
  status_file = open(generate_path("/src/flow/downlink_status.txt"), "wb")
  pickle.dump(status, status_file)
  status_file.close()

def generate_downlink_data():
  status = get_uplink_data()
  if status == AURORA_DATA:
    file_name = glob.glob(generate_path("/data/aurora_data/*"))[0]
    sending_data = make_data_for_downlink(file_name)
  elif len(status) == AURORA_IMG:
    if status == IMAGE_SEND_COMPLETE:
      print("complete")
      delete_files("/data/aurora_img")
    else:
      sending_data = make_data_for_downlink("/data/aurora_img/" + status[0] + ".txt")
  else:
    if status[1] == 0:
      sending_data = make_data_for_downlink("/data/aurora_img/" + status[0] + ".txt")
      "ダウンリンクは終了"
    else:
      sending_data = make_data_for_downlink("/data/aurora_img/" + status[0] + ".txt")
    sending_data = "消しました" #削除したことを伝えるデータを用意してダウンリンク→ダウンリンク終了
  return sending_data
