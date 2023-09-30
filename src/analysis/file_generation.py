import glob
import cv2
import numpy as np
from natsort import natsorted

from util import generate_path

def split_text_string(data_path, string_length=128):
  """.txtファイル内の文字列をn文字ごとに分割

  Args:
      data_path (str): artificial_satellite/からの相対パス
      string_length (int): 指定の文字数で分割
      
  Caution:
    バイナリー化されたデータは60文字ごとに改行されている
    改行コードを削除して読み込む必要がある。

  """
  absolute_img_path = generate_path(data_path)
  data = open(absolute_img_path, "r", encoding="utf-8").read()
  if '\n' in data:
    not_new_line_data = data.replace('\n', '')
  else:
    not_new_line_data = data
  split_str = [not_new_line_data[i:i+string_length] for i in range(0, len(not_new_line_data), string_length)]
  count = 1
  for i in split_str:
    packet = f'{generate_path("/data/aurora_img/")}{count}.txt'
    open(packet, "w").write(i)
    count += 1

def combine_string(relative_path, readline_length=60):
  """.txtファイル内の文字列同士を結合して1つの.txtファイルを作成

  Args:
    relative_path (str): artificial_satellite/からの相対パス
      e.g.) "/data/aurora_img/*.txt"

    readline_length (int): 1行に記入する文字列の長さ
      
  """
  all_aurora_data = ""
  aurora_data_paths = natsorted(glob.glob(generate_path(relative_path)))
  for aurora_data_path in aurora_data_paths:
    file = open(aurora_data_path, "r")
    aurora_data = file.read()
    all_aurora_data += aurora_data
  binary_data = ""
  read_lines = [all_aurora_data[i:i+readline_length] for i in range(0, len(all_aurora_data), readline_length)]
  for read_line in read_lines:
    binary_data += read_line + '\n'
  binary_data_path = generate_path("/data/restore.txt")
  open(binary_data_path, "w").write(binary_data)
  
def convert_img_into_text(relative_img_path):
  """画像をテキストデータに変換

  Arg:
    relative_img_path (str): artificial_satellite/からの相対パス
  """
  image_path = generate_path(relative_img_path)
  img = cv2.imread(image_path)
  hex_img_data = ""
  flatten_array = img.ravel()
  for element in flatten_array:
    hex_element = format(element, "x")
    if len(hex_element) == 1:
      hex_element = "0" + hex_element
    hex_img_data += hex_element
  with open(generate_path("/data/downlink_data.txt"), "w") as img_text_file:
    img_text_file.write(hex_img_data)

def restore_img(raw_data_relative_path, restore_relative_path, width, height):
  """テキストデータから画像復元

  Args:
    raw_data_relative_path (str): artificial_satellite/からの相対パス
    restore_relative_path (str): artificial_satellite/からの相対パス
    width (int): 横の画素数
    height (int): 縦の画素数
  """
  with open(generate_path(raw_data_relative_path), "r") as img_text_file:
    img_data = img_text_file.read()
  hex_pixel_array = [img_data[i:i+2] for i in range(0, len(img_data), 2)]
  pixel_array = np.array([])
  for hex_pixel_element in hex_pixel_array:
    pixel_element = int(hex_pixel_element, 16)
    pixel_array = np.append(pixel_array, pixel_element)
  img = np.reshape(pixel_array, (height, width, 3))
  cv2.imwrite(generate_path(restore_relative_path), img)

#a