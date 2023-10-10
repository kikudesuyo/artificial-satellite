import glob
from natsort import natsorted
from util import generate_path, delete_files

def merge_aurora_data(first_file_name, num_merged_files):
  """複数のオーロラデータを結合
  オーロラデータは1つあたり8byte
  
  Args:
    first_file_name (int): 最初のファイル番号
    num_merged_files (int): ファイルの結合数

  Return:
    merged_data (str):
  """
  merged_data = ""
  for file_name in range(first_file_name, first_file_name + num_merged_files):
    with open(generate_path(f"/data/aurora_data/{file_name}.txt"), "r") as aurora_data_file:
      aurora_data = aurora_data_file.read()
    merged_data += aurora_data
  return merged_data


