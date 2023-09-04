from shooting.take_photograph import take_photo
from format.uart_communication import receive_command, send_command
from util import shutdown, set_date_on_raspi, delete_files
from helper.file_operation import delete_files_amount
from helper.complemention import is_correct_time
from constant import ERROR_VALUE


def shooting_flow(time_date):
  try:
    is_correct_time(time_date) #取得したデータによって編集
    #time_dataを秒数に変換するプログラムを作成
  except:
    time_date = ERROR_VALUE
  delete_files_amount( "/img/shooting_img", threshold=2500)
  take_photo(time_date, 750, 2000) #緯度によって強制停止してもいいかもしれない（別のターミナルで）
  
  """
  command = receive_command("継続可能かどうか")
  if command == "シャットダウンか":
    return 0
  else:
    send_command("解析指示を受けました")
    return "解析継続"
  """