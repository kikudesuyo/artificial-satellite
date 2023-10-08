from downlink.downlink_status_edition import initialize_status
from constant.format import FORMAT_DATA_SIZE, FORMAT_DATA_START
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
  data_size = format_array[FORMAT_DATA_SIZE]
  if data_size % 3 == 0:
    pass
  else:
    print("uplink_data is broken")
    return None
  uplink_data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
  #配列のサイズを求めて配列を予め用意しておく。
  designed_files = []
  for index in range(0, len(uplink_data), ELEMTNTS_IMG_FILE_NUMBER):
    raw_img_number = uplink_data[index: index+ELEMTNTS_IMG_FILE_NUMBER]
    if len(raw_img_number) == ELEMTNTS_IMG_FILE_NUMBER:
      img_number = raw_img_number[0]*256 + raw_img_number[1]*16 + raw_img_number[2]
      designed_files.append(img_number)
  return designed_files