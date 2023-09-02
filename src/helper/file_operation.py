import glob
from util import generate_path

def get_amount(relative_path):
  amount = len(glob.glob(generate_path(relative_path + "/*")))
  return amount