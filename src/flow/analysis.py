from format.uart_communication import receive_command, send_command
from analysis.main import main as analysis_main
from util import shutdown, delete_files
from helper.file_operation import get_amount

def analysis_flow():
  send_command("解析指示を受けました")
  amount_aurora_data = get_amount("/data/aurora_data")
  if amount_aurora_data >= 1000:
    delete_files("/data/aurora_data")
  analysis_main()
  send_command("電力停止要求")
  receive_command("シャットダウン要求受信")
  shutdown()