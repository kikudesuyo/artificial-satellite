from shooting.take_photograph import take_photo
from helper.file_operation import delete_files_amount
from helper.complemention import is_correct_time
from constant import ERROR_VALUE


def shooting_flow(time_data):
  """

  Arg:
    time_data (list[int]): 4byteの時刻データ[week,hour,minute,second]
  """
  try:
    is_correct_time(time_data)
    satellite_time = time_data[0]*7*24*60*60 + time_data[1]*24*60*60 + time_data[2]*60*60 + time_data[3]*60
  except:
    satellite_time = ERROR_VALUE
  delete_files_amount( "/img/shooting_img", threshold=2500)
  take_photo(satellite_time, 10, 2000) #緯度によって強制停止してもいいかもしれない（別のターミナルで）
  
  """
  command = receive_command("継続可能かどうか")
  if command == "シャットダウンか":
    return 0
  else:i
    send_command("解析指示を受けました")
    return "解析継続"
  """