from shooting.take_photograph import take_photo
from helper.file_operation import delete_files_amount
from helper.complemention import is_correct_time
from constant import ERROR_VALUE


def shooting_flow(time_date):
  try:
    is_correct_time(time_date)
    satellite_time = int(time_date[:2], 16)*7*24*60*60 + int(time_date[2:4], 16)*24*60*60 + int(time_date[4:6], 16)*60*60 + int(time_date[6:8], 16)*60
  except:
    satellite_time = ERROR_VALUE
  delete_files_amount( "/img/shooting_img", threshold=2500)
  take_photo(satellite_time, 750, 2000) #緯度によって強制停止してもいいかもしれない（別のターミナルで）
  
  """
  command = receive_command("継続可能かどうか")
  if command == "シャットダウンか":
    return 0
  else:i
    send_command("解析指示を受けました")
    return "解析継続"
  """