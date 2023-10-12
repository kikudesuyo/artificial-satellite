from analysis.main import main as analysis_main
from util import delete_files
from helper.file_operation import delete_files_amount, output_raspi_status
from constant.status import ANALYSIS_INTERRUPTION, OTHERS_COMPLETION

def analysis_flow():
  output_raspi_status(ANALYSIS_INTERRUPTION)
  delete_files_amount("/data/aurora_data", threshold=1000)
  analysis_main()
  delete_files("/img/shooting_img")
  output_raspi_status(OTHERS_COMPLETION)