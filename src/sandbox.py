# from analysis.main import main

# main()
from helper.file_operation import delete_files_smaller_than_threshold
from downlink.status_edition import renew_status_file

# renew_status_file(1)
delete_files_smaller_than_threshold(4)