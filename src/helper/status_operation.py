from util import generate_path, delete_files
from flow.analysis import analysis_flow
from flow.split import split_flow
from format.format import send_CMD

from constant.status import SHOOTING_COMPLETION, OTHERS_COMPLETION, SHOOTING_INTERRUPTION, ANALYSIS_INTERRUPTION, SPLIT_INTERRUPTION
from constant.command_list import CMD_RPI_EPS_SHUTDOWN
from constant.format import EPS_ADDR, FORMAT_DATA_START

def handle_based_on_previous_status():
  with open(generate_path("/src/format/order.txt"), "r") as status_file:
    status = int(status_file.read())
    if status == SHOOTING_COMPLETION or status == SHOOTING_INTERRUPTION:
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

def is_equal_command(format_array, last_format_array):
  if format_array[:FORMAT_DATA_START] == last_format_array[:FORMAT_DATA_START]:
    return True
  else:
    return False
  
def does_front_handle():
  with open(generate_path("/src/format/order.txt"), "r") as status_file:
    status = int(status_file.read())
  if status != SHOOTING_COMPLETION and status != OTHERS_COMPLETION:
    return True
  else:
    return False