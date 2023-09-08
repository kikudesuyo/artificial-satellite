import glob
from util import generate_path, delete_files

def delete_files_amount(relative_path, threshold):
  amount = len(glob.glob(generate_path(relative_path + "/*")))
  if amount >= threshold:
    delete_files(relative_path)