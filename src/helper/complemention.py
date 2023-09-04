from constant import MIN_WEEK_RANGE, MAX_WEEK_RANGE, MIN_HOUR_RANGE, MAX_HOUR_RANGE, MIN_MINUTE_RANGE, MAX_MINUTE_RANGE, MIN_SECOND_RANGE, MAX_SECOND_RANGE

def complement_datetime(datetime):
  "送信データはYYYYMMDDhhmmssと仮定"
  "データが正しい型ではなかったら規定値を出力"
  try:
    datetime = datetime.zfill(14)
    year = int(datetime[:4])
    if not (2100 > year > 2000):
      raise Exception
    month = int(datetime[4:6])
    if not (12 >= month >= 1):
      raise Exception
    day = int(datetime[6:8])
    if not (31 >= day >= 1):
      raise Exception
    hour = int(datetime[8:10])
    if not (23 >= hour >= 0):
      raise Exception
    minute = int(datetime[10:12])
    if not (59 >= minute >= 0):
      raise Exception
    second = int(datetime[12:14])
    if not (59 >= second >= 0):
      raise Exception
    datetime = f'{year}{month}{day}{hour}{minute}{second}'
  except:
    datetime = "20000101000000"
  return datetime

# print(complement_datetime("20211021034523"))

from util import get_current_time

def calc_elasped_satellite_time(raw_satellite_time):
  """衛星時間を計測

  Args:
    raw_satellite_time (str): week+hour+minute+secondの4byte(16進数)
  Return:
    hex_satellite_time (str): 衛星時間(second) 16進数データ
  """
  sat_elasped_time = int(raw_satellite_time[0:1], 16)*7*24*60*60 + int(raw_satellite_time[2:4], 16)*60*60 + int(raw_satellite_time[4:6], 16)*60 + int(raw_satellite_time[3], 16)
  rpi_current_time = get_current_time()
  rpi_elasped_time = int(rpi_current_time[8:10])*60*60 + int(rpi_current_time[10:12])*60 + int(rpi_current_time[12:14])
  satellite_time = sat_elasped_time + rpi_elasped_time
  hex_satellite_time = hex(satellite_time)[2:]
  return hex_satellite_time


def is_correct_time(satellite_time):
  """衛星時間の正誤判定

  Arg:
    satellite_time (list[int]):
  """
  if not  MIN_WEEK_RANGE <= satellite_time[0] <= MAX_WEEK_RANGE:
    raise ValueError("Invalid data.")
  elif not  MIN_HOUR_RANGE <= satellite_time[1] <= MAX_HOUR_RANGE:
   raise ValueError("Invalid data.")
  elif not  MIN_MINUTE_RANGE <= satellite_time[2] <= MAX_MINUTE_RANGE:
    raise ValueError("Invalid data.")
  elif not  MIN_SECOND_RANGE <= satellite_time[3] <= MAX_SECOND_RANGE:
    raise ValueError("Invalid data.")
  else:
    return True