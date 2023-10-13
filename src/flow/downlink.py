from util import generate_path
from downlink.shape_up import split_string, merge_aurora_data
from downlink.status_edition import read_designed_packet, initialize_status
from constant.status import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, MERGED_AURORA_DATA_NUMBER

def read_file_contents(relative_path):
  with open(generate_path(relative_path), "r") as file:
    file_data = file.read()
  return file_data

def get_downlink_data(downlink_status):
  """

  Arg:
    downlink_status(int): 
      0:初期値, 1:オーロラデータ, 2:分割画像, 3:分割画像連番

  Return:
    downlink_data(str):
  Warning:
    取得失敗したらstatusファイルを全て初期化
  """
  try:
    if downlink_status == AURORA_DATA:
      aurora_data_status = int(read_file_contents("/src/status/aurora_data.txt"))
      downlink_data = merge_aurora_data(first_file_name=aurora_data_status, num_merged_files=MERGED_AURORA_DATA_NUMBER)
    elif downlink_status == AURORA_IMG:
      aurora_img_status = read_file_contents("/src/status/aurora_img.txt")
      downlink_data = read_file_contents(f"/data/aurora_img/{aurora_img_status}.txt")
    elif downlink_status == DESIGNED_AURORA_IMG:
      designed_img_status = read_designed_packet()[0]
      downlink_data = read_file_contents(f"/data/aurora_img/{designed_img_status}.txt")
    else:
      raise ValueError("downlink status doesn't exist. Initialize all status.")
  except Exception as e:
    print(e)
    initialize_status()
    return None
  sending_data = split_string(downlink_data)
  return sending_data