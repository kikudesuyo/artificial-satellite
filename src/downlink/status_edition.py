import re
import pickle
import glob
from natsort import natsorted

from util import generate_path
from helper.file_operation import read_file_contents, write_to_file
from constant.status import (INITIAL_DOWNLINK, AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, INIT_FILE_NUMBER,
INIT_DESIGNED_NUMS)

def write_uplink_info(uplink_data):
  uplink_data_str = [0]*len(uplink_data)
  for i in range(len(uplink_data)):
   uplink_data_str[i] = format(uplink_data[i],'02x')          
  info_data = ",".join(uplink_data_str)
  write_to_file(info_data, "/src/status/uplink_info.txt")

def check_uplink_info():
  uplink_info = read_file_contents("/src/status/uplink_info.txt")
  uplink_info = uplink_info.split(',')
  return uplink_info

def read_designed_packet():
  designed_img_file = open(generate_path("/src/status/designed_aurora_img.txt"), "rb")
  designed_files = pickle.load(designed_img_file)
  designed_img_file.close()
  return designed_files

def write_designed_nums(file_nums):
  """
  Arg:
  file_nums (list[int])
  """
  designed_img_file = open(generate_path("/src/status/designed_aurora_img.txt"), "wb")
  pickle.dump(file_nums, designed_img_file)
  designed_img_file.close()

def count_up(current_count, increment=1):
  """現在のcountからincrement分だけ増加"""
  return current_count + increment

def delete_initial_element(list):
  if len(list) != 0:
    list.pop(0)
  return list

def renew_status_file(downlink_status):
  """ダウンリンク後にstatusを変更
  ファイル数を確認
  """
  if downlink_status == AURORA_DATA:
    min_file_name = natsorted(glob.glob(generate_path("/data/aurora_data/*.txt")))[0]
    min_file_number = re.sub(r'\D', '', min_file_name)
    write_to_file(min_file_number, "/src/status/aurora_data.txt")
  elif downlink_status == AURORA_IMG:
    aurora_img_num = read_file_contents("/src/status/aurora_img.txt")
    write_to_file(str(count_up(int(aurora_img_num))), "/src/status/aurora_img.txt")
  elif downlink_status == DESIGNED_AURORA_IMG:
    designed_files = read_designed_packet()
    delete_initial_element(designed_files)
    write_designed_nums(designed_files)
  else:
    print("flow is wrong")

def initialize_status():
  """ダウンリンクに関するステータスを全て初期化"""
  write_to_file(str(INITIAL_DOWNLINK), "/src/status/downlink_status.txt")
  min_file_name = natsorted(glob.glob(generate_path("/data/aurora_data/*.txt")))[0]
  min_file_number = re.sub(r'\D', '', min_file_name)
  write_to_file(min_file_number, "/src/status/aurora_data.txt")
  write_to_file(str(INIT_FILE_NUMBER), "/src/status/aurora_img.txt")
  write_designed_nums(INIT_DESIGNED_NUMS)