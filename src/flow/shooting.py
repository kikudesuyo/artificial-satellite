from shooting.take_photograph import take_photo
from format.uart_communication import receive_command, send_command
from util import shutdown, set_date_on_raspi, delete_files
from helper.file_operation import delete_files_amount
from constant import INITIAL_TIME_DATA


def shooting_flow(time_date):
  try:
    date = hex(time_date) #取得したデータによって編集
    set_date_on_raspi(date)
  except:
    set_date_on_raspi(INITIAL_TIME_DATA)
  delete_files_amount("/img/shooting_img", threshold=2500)
  take_photo(750, 2000) #緯度によって強制停止してもいいかもしれない（別のターミナルで）
  send_command("継続可能かEPSに尋ねる")
  command = receive_command("継続可能かどうか")
  if command == "シャットダウンか":
    return 0
  else:
    send_command("解析指示を受けました")
    return "解析継続"