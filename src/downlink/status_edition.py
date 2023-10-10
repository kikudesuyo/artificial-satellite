import pickle
import glob
from natsort import natsorted

from util import generate_path
from constant.status import INITIAL_DOWNLINK, AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, INIT_FILE_NUMBER, INIT_DESIGNED_NUMS


def write_to_file(content, relative_file_path):
  with open(generate_path(relative_file_path), "w") as file:
    file.write(content)

def write_designed_nums(file_nums):
  """
  Arg:
  file_nums (list[int])
  """
  designed_img_file = open(generate_path("/src/status/designed_aurora_img.txt"), "wb")
  pickle.dump(file_nums, designed_img_file)
  designed_img_file.close()

def write_downlink_status(downlink_status):
  """何をダウンリンクするかをステータスファイルに保存
  
  Arg:
    downlink_status (int):
  """
  with open(generate_path("/src/status/downlink_status.txt"), "w") as status_file:
    status_file.write(str(downlink_status))

def check_status(relative_path):
  """

  Arg:
    relative_path (str)
  Return:
    status (int): ダウンリンクする対象
  """
  with open(generate_path(relative_path), "r") as status_file:
    status = int(status_file.read())
  return status

def is_continuing_downlink():
  """ダウンリンク継続か

  Return:
    bool
  """
  downlink_status = check_status("/src/status/downlink_status.txt") 
  if downlink_status == AURORA_DATA:
    file_qty = len(natsorted(glob.glob(generate_path("/data/aurora_data/*"))))
    aurora_data_status = check_status("/src/status/aurora_data.txt")
    left_file_qty = file_qty - aurora_data_status
  elif downlink_status == AURORA_IMG:
    file_qty = len(natsorted(glob.glob(generate_path("/data/aurora_img/*"))))
    aurora_img_status = check_status("/src/status/aurora_img.txt")
    left_file_qty = file_qty - aurora_img_status
  elif downlink_status == DESIGNED_AURORA_IMG:
    left_file_qty = len(read_designed_packet())
  elif downlink_status == INITIAL_DOWNLINK:
    print("flow is wrong")
    return False
  else:
    print("downlink status file broken")
    write_downlink_status(INITIAL_DOWNLINK)
    return False
  if left_file_qty > 0:
    print("downlink continue")
    return True
  else:
    print("downlink finish")
    return False

def count_up(current_count):
  return current_count + 1

def delete_initial_element(list):
  list.pop(0)
  return list

def change_status_file(downlink_status):
  """ダウンリンク後にstatusを変更
  ファイル数を確認
  """
  if downlink_status == AURORA_DATA:
    with open(generate_path("/src/status/aurora_data.txt"), "r") as aurora_data_status:
      aurora_data_num = aurora_data_status.read()
    with open(generate_path("/src/status/aurora_data.txt"), "w") as aurora_data_status:
      aurora_data_status.write(str(count_up(int(aurora_data_num))))
  elif downlink_status == AURORA_IMG:
    with open(generate_path("/src/status/aurora_img.txt"), "r") as aurora_img_status:
      aurora_img_num = aurora_img_status.read()
    with open(generate_path("/src/status/aurora_img.txt"), "w") as aurora_img_status:
      aurora_img_status.write(str(count_up(int(aurora_img_num))))
  elif downlink_status == DESIGNED_AURORA_IMG:
    designed_files = read_designed_packet()
    delete_initial_element(designed_files)
    designed_img_file = open(generate_path("/src/status/designed_aurora_img.txt"), "wb")
    pickle.dump(designed_files, designed_img_file)
    designed_img_file.close()
  else:
    print("flow is wrong")


def read_designed_packet():
  designed_img_file = open(generate_path("/src/status/designed_aurora_img.txt"), "rb")
  designed_files = pickle.load(designed_img_file)
  designed_img_file.close()
  return designed_files

def initialize_status():
  """ダウンリンクに関するステータスを全て初期化"""
  with open(generate_path("/src/status/downlink_status.txt"), "w") as file:
    file.write(str(INITIAL_DOWNLINK))
  with open(generate_path("/src/status/aurora_data.txt"), "w") as file:
    file.write(str(INIT_FILE_NUMBER))
  with open(generate_path("/src/status/aurora_img.txt"), "w") as file:
    file.write(str(INIT_FILE_NUMBER))
  write_designed_nums(INIT_DESIGNED_NUMS)