from helper.file_operation import delete_files_smaller_than_threshold
from downlink.status_edition import renew_status_file, write_designed_nums
from downlink.shape_up import merge_aurora_data
from util import generate_path
#オーロラデータのテキストの値とマージする数を足したものを引数とすればOK
# delete_files_smaller_than_threshold(5)

from flow.split import split_flow

# split_flow()
from analysis.main import main

# for _ in range(1, 11):
#   main()

# delete_files_smaller_than_threshold(5)
from downlink.status_edition import initialize_status, renew_status_file, read_designed_packet, write_designed_nums
from helper.file_operation import read_file_contents
from constant.status import MERGED_AURORA_DATA_NUMBER
write_designed_nums([12, 453, 53, 43])
# initialize_status()
print(read_designed_packet())
initialize_status()
print(read_designed_packet())