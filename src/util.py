from pathlib import Path
import os
import shutil
import glob
import subprocess

def generate_path(path):
  """絶対パスを生成

  Arg:
    path (str): artificial_satellite/からの相対パス

  Return:
    str: 引数pathへの絶対パス
  """
  return str(Path(__file__).parents[1]) + path

def delete_files(directory_path):
  """指定のディレクトリ内に存在するファイルを削除
  
  Caution:
    削除したファイルは復元不可能
    
  Arg:
    directory_path(str): artificial_satellite/からの相対パス 
  """
  absolute_path = generate_path(directory_path)
  full = len(glob.glob(absolute_path + "/*"))
  only_extension = len(glob.glob(absolute_path + "/*.*"))
  if full != only_extension:
    raise IsADirectoryError("Error!!指定したディレクトリの中にディレクトリが存在します。")
  shutil.rmtree(absolute_path)
  os.makedirs(absolute_path)
  
def shutdown():
  """
  
  Caution:
    bashコマンドでのみ使用可能
  """
  subprocess.run(['sudo', 'shutdown', 'now'])
  
def copy_file(source_path, copy_path):
  subprocess.run(["cp", source_path, copy_path])
  

def convert_datetime_to_hex_seconds(datetime = "DDhhmmss"):
  day = int(datetime[:2])
  hour = int(datetime[2:4])
  minute = int(datetime[4:6])
  second = int(datetime[6:8])
  datetime_seconds = day * 24 * 3600 + hour * 3600 + minute * 60 + second
  hex_datetime_seconds = format(datetime_seconds, "x").zfill(6)
  return hex_datetime_seconds

def restore_hex_seconds_to_datetime(hex_seconds):
  """

  Arg:
      hex_seconds (str): 16進数時刻データ("DDhhmmss")
      
  Return:
      datetime (str): "DDhhmmss"
  """
  seconds = int(hex_seconds, 16)
  day, day_remainder = seconds // (24 * 3600), seconds % (24 * 3600)
  hour, hour_remainder = day_remainder // 3600, day_remainder % 3600
  minute, second = hour_remainder // 60, hour_remainder % 60
  datetime = f'{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}'
  return datetime