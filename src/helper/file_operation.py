import os
import glob
import re
from natsort import natsorted

from util import generate_path, delete_files, delete_file

def delete_files_amount(relative_path, threshold):
  amount = len(glob.glob(generate_path(relative_path + "/*")))
  if amount >= threshold:
    delete_files(relative_path)

def output_raspi_status(status):
  write_to_file(status, "/src/status/raspi_status.txt")

def write_to_file(content, relative_file_path):
  with open(generate_path(relative_file_path), "w") as file:
    file.write(content)

def read_file_contents(relative_path):
  with open(generate_path(relative_path), "r") as file:
    contents = file.read()
  return contents

def delete_files_smaller_than_threshold(threshold):
  files = natsorted(glob.glob(generate_path("/data/aurora_data/*.txt")))
  deleted_paths = list(filter(lambda path: int(re.sub(r'\D', '', path)) < threshold, files))
  for deleted_path in deleted_paths:
    delete_file(deleted_path)