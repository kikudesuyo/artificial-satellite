from util import generate_path, delete_files, shutdown
from flow.analysis import analysis_flow
from flow.split import split_flow
from format.format import send_CMD

from constant import SHOOTING_COMPLETION, SHOOTING_INTERRUPTION, ANALYSIS_INTERRUPTION, SPLIT_INTERRUPTION
from constant import EPS_ADDR
from format.YOTSUBA_CMD_RPI import CMD_RPI_EPS_SHUTDOWN

def handle_based_on_previous_status():
  with open(generate_path("/src/format/order.txt", "r")) as status_file:
    status = status_file.read()
    if status == SHOOTING_COMPLETION or SHOOTING_INTERRUPTION:
      analysis_flow()
    elif status == ANALYSIS_INTERRUPTION:
      delete_files("/data/aurora_data")
      analysis_flow()
    elif status == SPLIT_INTERRUPTION:
      delete_files("/data/aurora_img")
      split_flow()
    else:
      return 
    print("shutdown")
    send_CMD(EPS_ADDR, CMD_RPI_EPS_SHUTDOWN)
    #shutdown()
    

