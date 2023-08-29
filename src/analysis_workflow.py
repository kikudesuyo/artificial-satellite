from format.uart_communication import receive_command, send_command
from analysis.main import main as analysis_main
from util import shutdown

def alanasis_flow():
  send_command("解析指示を受けました")
  analysis_main()
  send_command("電力停止要求")
  receive_command("シャットダウン要求受信")
  shutdown()