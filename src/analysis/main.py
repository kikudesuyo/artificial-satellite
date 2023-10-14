from natsort import natsorted
import glob
from util import generate_path, delete_file
from analysis.aurora_evaluation import make_aurora_data

def main():
  """
  画像読み込み→解析→テキスト出力→画像破棄
  
  内部の関数で最適画像を選定(make_aurora_data())
  """
  img_path = natsorted(glob.glob(generate_path("/img/shooting_img/*.jpg")))[0]
  aurora_data = make_aurora_data(img_path)
  file_number = len(glob.glob(generate_path("/data/aurora_data/*.txt"))) + 1
  raw_date_time, raw_aurora_rate, raw_hue, raw_saturation, raw_value = aurora_data
  date_time = hex(int(raw_date_time))[2:].zfill(8)
  hex_aurora_percentage = format(int(round(raw_aurora_rate, 2) *100), "x").zfill(2)
  hex_hue = format(int(raw_hue), "x").zfill(2)
  hex_saturation = format(int(raw_saturation), "x").zfill(2)
  hex_value = format(int(raw_value), "x").zfill(2)
  with open(generate_path(f'/data/aurora_data/{file_number}.txt'), "w") as text_file:
    text_file.write(date_time + hex_aurora_percentage + hex_hue + hex_saturation + hex_value)
  delete_file(img_path)