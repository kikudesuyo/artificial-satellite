import glob
from util import generate_path, delete_files

def delete_files_amount(relative_path, threshold):
  amount = len(glob.glob(generate_path(relative_path + "/*")))
  if amount >= threshold:
    delete_files(relative_path)

def output_raspi_status(status):
  with open(generate_path("/src/status/raspi_status.txt"), "w") as status_file:
    status_file.write(str(status))
