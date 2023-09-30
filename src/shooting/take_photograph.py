import subprocess
import time

from util import generate_path
from shooting.time_relation import calc_elasped_satellite_time

def take_photo(elasped_time, shooting_times, interval_msec, width_size=1960, height_size=1080):
  """撮影

  Args:
    elasped_time (int): 経過時刻
    shooting_times (int): 撮影回数
    interval_msec (int): 撮影間隔(ミリ秒) 
    width_size (int): 縦画素数
    height_size (int): 横画素数
  """
  start = time.perf_counter()
  img_dir_path = generate_path("/img/shooting_img/")
  for _ in range(shooting_times):
    #画像のファイル名は衛星時刻(16進数の4byteデータ)にする
    end = time.perf_counter()
    execute_time = end - start
    file_name = hex(int(elasped_time + execute_time))[2:]
    file_path = img_dir_path + file_name + ".jpg"
    subprocess.run(['raspistill', '-o', file_path, '-t', str(interval_msec), '-w', str(width_size), '-h', str(height_size)])
