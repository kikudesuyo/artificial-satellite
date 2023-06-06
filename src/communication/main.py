import glob

from communication.spi_master import init, send_data
from util import generate_path

def get_aurora_data(path):
  """/*.txtの内容をリストに出力

  Arg:
    path (str): /artificial_sattellite/ からの相対パス 
  Return:
    aurora_data(list): 10進数のオーロラデータ
  """
  aurora_values = []
  aurora_data_paths = glob.glob(generate_path(path))
  for aurora_data_path in aurora_data_paths:
    file = open(aurora_data_path, "r")
    aurora_value = int(float(file.read()))
    aurora_values.append(aurora_value)
  return aurora_values

def main():   
  aurora_values = get_aurora_data("/data/packet/*.txt")
  init()
  for aurora_value in aurora_values:
    send_data(aurora_value)
  