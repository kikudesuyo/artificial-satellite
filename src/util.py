from pathlib import Path
import datetime
import re
import os
import shutil
import glob

def generate_path(path):
  """絶対パスを生成

  Arg:
    path (str): artificial_satellite/からの相対パス

  Return:
      str: 引数pathへの絶対パス
  """
  return str(Path(__file__).parents[1]) + path

def get_current_time():
  """実装する際にcurrnt timeではなく撮影した時刻を取得する
  .nowではなく撮影した画像ファイル名から時刻を取得する
  """
  row_time_data = str(datetime.datetime.now())
  time_data = row_time_data[:row_time_data.find(".")]
  current_time = re.sub(r"\D", "", time_data)
  return current_time

def delete_files(path):
  """ディレクトリに存在するファイルを削除
  
  Causion:
    削除したファイルは復元不可能
    
  Arg:
    path(str): artificial_satellite/からの相対パス
  """
  absolute_path = generate_path(path)
  full = len(glob.glob(absolute_path + "/*"))
  only_extension = len(glob.glob(absolute_path + "/*.*"))
  if full != only_extension:
    raise IsADirectoryError("Error!!指定したディレクトリの中にディレクトリが存在します。")
  shutil.rmtree(absolute_path)
  os.makedirs(absolute_path) 