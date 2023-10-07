from constant.shooting import (MIN_WEEK_RANGE, MAX_WEEK_RANGE, MIN_HOUR_RANGE,
MAX_HOUR_RANGE, MIN_MINUTE_RANGE, MAX_MINUTE_RANGE, MIN_SECOND_RANGE, MAX_SECOND_RANGE,
SHOOTING_DURATION_SECOND)

def is_correct_time(satellite_time):
  """衛星時間の正誤判定

  Arg:
    satellite_time (list[int]):
  """
  if not  MIN_WEEK_RANGE <= satellite_time[0] <= MAX_WEEK_RANGE:
    raise ValueError("Invalid mc time data.")
  elif not  MIN_HOUR_RANGE <= satellite_time[1] <= MAX_HOUR_RANGE:
   raise ValueError("Invalid mc time data.")
  elif not  MIN_MINUTE_RANGE <= satellite_time[2] <= MAX_MINUTE_RANGE:
    raise ValueError("Invalid mc time data.")
  elif not  MIN_SECOND_RANGE <= satellite_time[3] <= MAX_SECOND_RANGE:
    raise ValueError("Invalid mc time data.")
  else:
    return True

def decrypt_to_satellite_time(time_data):
  """秒数データに変換

  Arg:
    time_data(list[int]): [week, hour, minute, second]からなる配列  
    
  Return:
    satellite_time(int): time_dataの秒数変換
  """
  satellite_time = time_data[0]*7*24*60*60 + time_data[1]*60*60 + time_data[2]*60 + time_data[3]
  return satellite_time

def is_shooting(start_time, current_time):
  """撮影継続か
  
  Args:
    start_time (int): 撮影開始時刻(秒)
    current_time (int): 現在の時刻(秒)
  """
  shooting_duration = current_time - start_time
  if shooting_duration > SHOOTING_DURATION_SECOND:
    return False
  else:
    return True
