from shooting.take_photograph import take_photo
from format.uart_communication import receive_command
from format.uart_communication import send_command
from util import shutdown, set_date_on_raspi


def shooting_flow():
    send_command("撮影指示の受信完了")
    row_date = receive_command()
    date = hex(row_date)
    set_date_on_raspi(date)
    take_photo(750, 2000) #緯度によって強制停止してもいいかもしれない（別のターミナルで）
    send_command("継続可能かEPSに尋ねる")
    command = receive_command("継続可能かどうか")
    if command == "シャットダウンか":
        return 0
        shutdown()
    else:
        return "解析継続"