from helper.file_operation import delete_files_smaller_than_threshold
from downlink.status_edition import renew_status_file, write_designed_nums
from downlink.shape_up import merge_aurora_data

#オーロラデータのテキストの値とマージする数を足したものを引数とすればOK
# delete_files_smaller_than_threshold(5)

from flow.split import split_flow

split_flow()
# from analysis.main import main

# main()

