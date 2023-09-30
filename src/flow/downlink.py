import glob
from natsort import natsorted

from util import delete_files
from constant.format import FORMAT_DATA_SIZE, FORMAT_DATA_START
from constant.status import AURORA_DATA, AURORA_IMG
from downlink.shape_up import make_data_for_downlink
from util import generate_path

# def generate_downlink_data():
#   """ステータスファイルを毎回確認してダウンリンクするデータを返り値にもたせる
#   """
#   status = AURORA_DATA
#   if status == AURORA_DATA:
#     downlink_number = check_status_file()
#     file_full_path = natsorted(glob.glob(generate_path("/data/aurora_data/*")))[downlink_number]
#     sending_data = make_data_for_downlink(file_full_path)
#   elif len(status) == AURORA_IMG:
#     if status == IMAGE_SEND_COMPLETE:
#       print("complete")
#       delete_files("/data/aurora_img")
#     else:
#       sending_data = make_data_for_downlink("/data/aurora_img/" + status[0] + ".txt")
#   else:
#     if status[1] == 0:
#       sending_data = make_data_for_downlink("/data/aurora_img/" + status[0] + ".txt")
#       "ダウンリンクは終了"
#     else:
#       sending_data = make_data_for_downlink("/data/aurora_img/" + status[0] + ".txt")
#     sending_data = "消しました" #削除したことを伝えるデータを用意してダウンリンク→ダウンリンク終了
#   return sending_data

def generate_downlink_data():
  file_full_path = glob.glob(generate_path("/data/aurora_data/*"))[0]
  print(file_full_path)
  sending_data = make_data_for_downlink(file_full_path)
  return sending_data

from downlink.uplink_edition import check_uplink_data_type, make_img_numbers, write_designed_status
from downlink.downlink_status_edition import write_downlink_status
from constant.status import DESIGNED_AURORA_IMG, AURORA_DATA, AURORA_IMG


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
