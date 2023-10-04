import glob
from constant.status import AURORA_DATA, AURORA_IMG
from downlink.shape_up import split_string
from util import generate_path
from downlink.uplink_edition import check_uplink_data_type, make_img_numbers
from downlink.downlink_status_edition import write_downlink_status, read_designed_packet, initialize_status
from constant.status import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG

#format_array = [7, 4, 0, 12, 43]
def handle_uplink_data(format_array):
  data_type = check_uplink_data_type(format_array)
  write_downlink_status(data_type)
  if data_type == AURORA_DATA:
    with open(generate_path("/src/status/aurora_data.txt"), "w") as status_file:
      status_file.write("1")
  elif data_type == AURORA_IMG:
    designed_file = make_img_numbers(format_array)[0]
    with open(generate_path("/src/status/aurora_img.txt"), "w") as status_file:
      status_file.write(str(designed_file))
  elif data_type == DESIGNED_AURORA_IMG:
    designed_files = make_img_numbers(format_array)
    write_designed_status(designed_files)
  else:
    print("uplink data is broken")

def read_file_contents(relative_path):
  with open(generate_path(relative_path), "r") as file:
    file_data = file.read()
  return file_data

def get_downlink_data():
  """
  Return:
    downlink_data(str):
  Warning:
    取得失敗したらstatusファイルを全て初期化
  """
  try:
    downlink_status = int(read_file_contents("/src/status/downlink_status.txt"))
    if downlink_status == AURORA_DATA:
      aurora_data_status = read_file_contents("/src/status/aurora_data.txt")
      downlink_data = read_file_contents(f"/data/aurora_data/{aurora_data_status}.txt")
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