from shooting.take_photograph import take_photo
from format.uart_communication import receive_command, send_command
from util import shutdown, set_date_on_raspi, delete_files
from helper.file_operation import get_amount


def shooting_flow():
  send_command("撮影指示の受信完了")
  row_date = receive_command()
  date = hex(row_date)
  set_date_on_raspi(date)
  amount_img = get_amount("/img/shooting_img")
  if amount_img >= 2000:
    delete_files("/img/shooting_img")
  take_photo(750, 2000) #緯度によって強制停止してもいいかもしれない（別のターミナルで）
  send_command("継続可能かEPSに尋ねる")
  command = receive_command("継続可能かどうか")
  if command == "シャットダウンか":
    shutdown()
    return 0
  else:
    return "解析継続"