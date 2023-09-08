import glob
from natsort import natsorted

from util import generate_path

def make_data_for_downlink(full_path):
  """１つのパケットを送信用に生成
  Arg:
    full_path (str): GSからのデータ（ファイル名）

  Return:
    downlink_data (list[int]): 0~255までの整数型配列
  """
  with open(generate_path(full_path), "r") as aurora_file:
    aurora_data = aurora_file.read()
    downlink_data = [int(aurora_data[x:x+2], 16) for x in range(0, len(aurora_data), 2)]
  return downlink_data
  
def get_splited_data(relative_path):
  """.txtデータをリストに格納

  Arg:
    relative_path (str): artificial_satellite/からの相対パス
  Return:
    splited_data (list[str])
  """
  data_paths = natsorted(glob.glob(generate_path(relative_path)))
  splited_data = []
  for data_path in data_paths:
    with open(data_path,  "r") as text_file:
      text_data = text_file.read()
      splited_data.append(text_data)
  return splited_data