from constant.shooting import (MIN_WEEK_RANGE, MAX_WEEK_RANGE, MIN_HOUR_RANGE,
MAX_HOUR_RANGE, MIN_MINUTE_RANGE, MAX_MINUTE_RANGE, MIN_SECOND_RANGE, MAX_SECOND_RANGE)

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