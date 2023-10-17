import os
import glob
import re
from natsort import natsorted

from util import generate_path, delete_all_files, delete_file

def write_to_file(content, relative_file_path):
  with open(generate_path(relative_file_path), "w") as file:
    file.write(content)

def read_file_contents(relative_path):
  with open(generate_path(relative_path), "r") as file:
    contents = file.read()
  return contents

def is_directory_not_empty(relative_directory_path):
  absolute_path = generate_path(relative_directory_path)
  if os.path.exists(absolute_path):
    return any(os.listdir(absolute_path))
  else:
    return False

def delete_files_amount(relative_path, threshold):
  amount = len(glob.glob(generate_path(relative_path + "/*")))
  if amount >= threshold:
    delete_all_files(relative_path)

def delete_files_smaller_than_threshold(threshold):
  """閾値よりも小さいファイル番号を削除"""
  files = natsorted(glob.glob(generate_path("/data/aurora_data/*.txt")))
  deleted_paths = list(filter(lambda path: int(re.sub(r'\D', '', path)) < threshold, files))
  for deleted_path in deleted_paths:
    delete_file(deleted_path)