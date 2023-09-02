from format.uart_communication import receive_command, send_command
from util import shutdown
import time

while True:
  command = receive_command()
  if command == "シャットダウン要求":
    send_command("電力停止要求")
    shutdown()
  
  time.sleep(5)