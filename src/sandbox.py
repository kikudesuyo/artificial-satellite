from helper.file_operation import delete_files_smaller_than_threshold
from downlink.status_edition import renew_status_file, write_designed_nums
from downlink.shape_up import merge_aurora_data

#オーロラデータのテキストの値とマージする数を足したものを引数とすればOK
# delete_files_smaller_than_threshold(5)

from flow.split import split_flow

# split_flow()
# from analysis.main import main

# main()

import subprocess
from util import generate_path
import glob

def delete_all_files(directory_path):
  full = len(glob.glob(directory_path + "/*"))
  only_extension = len(glob.glob(directory_path + "/*.*"))
  if full != only_extension:
    raise IsADirectoryError("Error!!指定したディレクトリの中にディレクトリが存在します。")
  subprocess.run(['sudo', 'rm', '-r', directory_path], check=True)

delete_all_files(generate_path("/data/aurora_data"))