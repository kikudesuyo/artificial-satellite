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
  
def convert_datetime_to_hex_seconds(datetime = "DDhhmmss"):
  day = int(datetime[:2])
  hour = int(datetime[2:4])
  minute = int(datetime[4:6])
  second = int(datetime[6:8])
  datetime_seconds = day * 24 * 3600 + hour * 3600 + minute * 60 + second
  hex_datetime_seconds = format(datetime_seconds, "x").zfill(6)
  return hex_datetime_seconds