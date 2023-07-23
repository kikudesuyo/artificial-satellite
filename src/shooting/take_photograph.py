import subprocess

from util import generate_path, get_current_time

def take_photo(shooting_times, shooting_interval_msec, width_size=1960, height_size=1080):
  """撮影

  Args:
      shooting_times (int): 撮影回数
      shooting_interval_msec (int): 撮影間隔(ミリ秒) 
      width_size (int): 縦画素数
      height_size (int): 横画素数
  """
  img_dir_path = generate_path("/img/shooting_img/")
  for _ in range(shooting_times):
    #画像のファイル名を時刻データにする
    #型は/DDhhmmss.jpg
    shooting_time = get_current_time()[6:]
    img_path = img_dir_path + shooting_time
    subprocess.run(['raspistill', '-o', img_path, '-t', shooting_interval_msec, '-w', str(width_size), '-h', str(height_size)])