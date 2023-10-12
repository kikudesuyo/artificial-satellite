from shooting.take_photograph import take_photo
from shooting.time_relation import is_correct_time
from helper.file_operation import delete_files_amount
from constant.shooting import ERROR_VALUE


def shooting_flow(satellite_time):
  """
  Arg:
    satellite_time (int): 経過時間(秒)
  """
  try:
    is_correct_time(satellite_time)
  except:
    satellite_time = ERROR_VALUE
  delete_files_amount( "/img/shooting_img", threshold=2500)
  take_photo(satellite_time, 2, 2000)