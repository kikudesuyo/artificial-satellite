import glob

from util import generate_path

def get_aurora_data(relative_path):
  """オーロラデータを読み込む

  Arg:
    relative_path (str): artificial_satellite/からの相対パス

  Return:
    splited_string (list[str]): 
  """
  
  all_aurora_data = ""
  aurora_data_paths = glob.glob(generate_path(relative_path))
  for aurora_data_path in aurora_data_paths:
    with open(aurora_data_path, "r") as aurora_file:
      aurora_data = aurora_file.read()
    all_aurora_data += aurora_data
  splited_string = split_string(all_aurora_data)
  return splited_string

def split_string(string, string_length=128):
  """オーロラデータを配列に格納

  Args:
      string (str): 16進数のオーロラデータ
      string_length (int, optional): 要素の文字数 Defaults to 128.

  Return:
      splited_string (list):
  """
  splited_string = [string[i: i+string_length] for i  in range(0, len(string), string_length)]
  return splited_string
  
def convert_msb_into_lsb(msb_binary_data):
  """1バイト毎に最上位ビットを最下位ビットに変換

  Arg:
    msb_binary_data(str): 
  Return:
    lsb_binary_data(str):
    
  ex)
    msb_binary_data = "0123456789abcdef"
    lsb_binary_data = "76543210fedcba98"
  """
  lsb_binary_data = ""
  lsb_one_byte_data = ""
  count = 1
  for msb_bit_data in msb_binary_data:
    lsb_one_byte_data = msb_bit_data + lsb_one_byte_data
    if len(lsb_one_byte_data) % 8 == 0:
      lsb_binary_data += lsb_one_byte_data
      lsb_one_byte_data = ""
    elif count == len(msb_binary_data) and count % 8 != 0:
      lsb_binary_data += lsb_one_byte_data
    count += 1
  return lsb_binary_data

def get_binary_data(aurora_data, msb=True):
  """

  Args:
      aurora_data (str): 16進数データ
      msb (bool, optional): 最上位ビットor最下位ビットを選択. Defaults to True.
  Return:
    binary_data(str): 
  """
  int_data = int(aurora_data, 16)
  binary_data = format(int_data, '04b')
  while len(binary_data) % 4 != 0:
      binary_data = "0" + binary_data
  if msb:
    pass
  else:
    binary_data = convert_msb_into_lsb(binary_data)
  return binary_data

def get_splited_data(relative_path):
  """.txtデータをリストに格納

  Arg:
    relative_path (str): artificial_satellite/からの相対パス
  Return:
    splited_data (list[str])
  """
  data_paths = glob.glob(generate_path(relative_path)) 
  splited_data = []
  for data_path in data_paths:
    with open(data_path,  "r") as text_file:
      text_data = text_file.read()
      splited_data.append(text_data)
  return splited_data