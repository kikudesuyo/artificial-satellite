from format.uart_communication import receive_command, send_command
from analysis.main import main as analysis_main
from util import shutdown, delete_files
from helper.file_operation import delete_files_amount

def analysis_flow():
  delete_files_amount("/data/aurora_data", threshold=1000)
  analysis_main()
  delete_files("/img/shooting_img")