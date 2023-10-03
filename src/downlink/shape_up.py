import glob
from natsort import natsorted

from util import generate_path

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
  
def store_for_downlink(relative_path):
  """16進数文字列を2文字ごとに分割した後にint型に変換して格納

  Arg:
    relative_path (str): artificial_satellite/からの相対パス
  Return:
    format_data (list[list[str]]): 1バイトを要素とする配列とし、.txtを1つの要素とする2重配列
      e.g.) format_data = [1.txt, 2.txt, 3.txt, 4.txt]
            1.txt = [12, 34, 56, 78]
  """
  downlink_data = get_splited_data(relative_path)
  format_data = []
  for packet in downlink_data:
    splited_packet = [int(packet[x:x+2], 16) for x in range(0, len(packet), 2)]
    format_data.append(splited_packet)
  return format_data

def split_string(string):
  """ダウンリンクするために文字列を配列に格納
  
  Arg:
    string (str):
  Return:
    format_data (list[int])
  """
  print(string)
  format_data = [int(string[x:x+2], 16) for x in range(0, len(string), 2)]
  return format_data
