# from format.format import get_data_from_format
from downlink.status_edition import write_to_file, write_designed_nums, initialize_status
from constant.format import FORMAT_DATA_SIZE, FORMAT_DOWNLINK_TYPE
from constant.status import AURORA_DATA, AURORA_IMG, DESIGNED_AURORA_IMG, AURORA_DATA_SIZE, ELEMTNTS_IMG_FILE_NUMBER


def check_uplink_data_type(format_array):
  try:
    data_size = format_array[FORMAT_DATA_SIZE]
    if data_size == AURORA_DATA_SIZE:
      return AURORA_DATA
    elif data_size == ELEMTNTS_IMG_FILE_NUMBER:
      return AURORA_IMG
    elif data_size % ELEMTNTS_IMG_FILE_NUMBER == 0 and data_size != ELEMTNTS_IMG_FILE_NUMBER:
      return DESIGNED_AURORA_IMG
    else:
      raise ValueError("uplink data is broken")
  except:
    initialize_status()
    return None

def make_img_numbers(format_array):
  """format_arrayから画像の番号を取得
  
  Arg:
    format_array(list[int])
  
  Return:
    designed_files(list[int])

  Explanation:
    uplink_data(list[int]):
      [データの種類, ファイル番号, ファイル番号, ファイル番号, ...]

  """
  data_size = format_array[FORMAT_DATA_SIZE]
  if data_size != 1 and data_size % 3 == 1:
    pass
  else:
    print("uplink_data is broken")
    return None
  uplink_data = format_array[FORMAT_DOWNLINK_TYPE: FORMAT_DOWNLINK_TYPE + format_array[FORMAT_DATA_SIZE]]
  #配列のサイズを求めて配列を予め用意しておく。
  designed_files = []
  for index in range(0, len(uplink_data), ELEMTNTS_IMG_FILE_NUMBER):
    raw_img_number = uplink_data[index: index+ELEMTNTS_IMG_FILE_NUMBER]
    if len(raw_img_number) == ELEMTNTS_IMG_FILE_NUMBER:
      img_number = raw_img_number[0]*256 + raw_img_number[1]*16 + raw_img_number[2]
      designed_files.append(img_number)
  return designed_files

def write_uplink_data_to_status(downlink_status, format_array):
  """アップリンクデータを基にステータスファイルに書き込み"""
  if downlink_status == AURORA_DATA:
    write_to_file("1", "/src/status/aurora_data.txt")
  elif downlink_status == AURORA_IMG:
    file_number = make_img_numbers(format_array)[0]
    write_to_file(str(file_number), "/src/status/aurora_img.txt")
  elif downlink_status == DESIGNED_AURORA_IMG:
    designed_files = make_img_numbers(format_array)
    write_designed_nums(designed_files)
  else:
    print("uplink_data is broken")
