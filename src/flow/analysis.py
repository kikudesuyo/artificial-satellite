from format.uart_communication import receive_command, send_command
from analysis.main import main as analysis_main
from util import shutdown, delete_files
from helper.file_operation import get_amount

def analysis_flow():
  amount_aurora_data = get_amount("/data/aurora_data")
  if amount_aurora_data >= 1000:
    delete_files("/data/aurora_data")
  analysis_main()
  delete_files("/img/shooting_img")