from downlink.shape_up import read_file_contents
from downlink.status_edition import renew_status_file
from helper.file_operation import delete_files_smaller_than_threshold
from constant.status import MERGED_AURORA_DATA_NUMBER, AURORA_DATA

downlink_status = 1
if downlink_status == AURORA_DATA:
  initial_file_name = read_file_contents("/src/status/aurora_data.txt")
  if initial_file_name != "":
    delete_files_smaller_than_threshold(int(initial_file_name)+MERGED_AURORA_DATA_NUMBER)
renew_status_file(downlink_status)        



