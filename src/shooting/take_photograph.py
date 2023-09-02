import subprocess

from util import generate_path
from helper.complemention import calc_elasped_satellite_time

def take_photo(shooting_times, interval_msec, width_size=1960, height_size=1080):
  """撮影

  Args:
      shooting_times (int): 撮影回数
      interval_msec (int): 撮影間隔(ミリ秒) 
      file_name (str):
      width_size (int): 縦画素数
      height_size (int): 横画素数
  """
  img_dir_path = generate_path("/img/shooting_img/")
  for _ in range(shooting_times):
    #画像のファイル名は衛星時刻(16進数の4byteデータ)にする
    with open(generate_path("/data/satellite_time.txt"), "r") as file:
      raw_satellite_time = file.read()
    filename = calc_elasped_satellite_time(raw_satellite_time)
    file_path = img_dir_path + filename + ".img"
    subprocess.run(['raspistill', '-o', file_path, '-t', interval_msec, '-w', str(width_size), '-h', str(height_size)])