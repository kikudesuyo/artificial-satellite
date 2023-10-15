# from analysis.main import main

# main()
from helper.file_operation import delete_files_smaller_than_threshold
from downlink.status_edition import renew_status_file, write_designed_nums
from downlink.shape_up import merge_aurora_data


print(merge_aurora_data(4, 4))

renew_status_file(3)
