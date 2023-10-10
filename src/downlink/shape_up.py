from util import generate_path

def split_string(string):
  """ダウンリンクするために文字列を配列に格納
  
  Arg:
    string (str):
  Return:
    format_data (list[int]): 1byteを1つの要素
      e.g.) format_data = [15, 3d, a1, 93]
  """
  print(string)
  format_data = [int(string[x:x+2], 16) for x in range(0, len(string), 2)]
  return format_data

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
