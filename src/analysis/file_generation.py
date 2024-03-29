import glob
import cv2
import numpy as np
from natsort import natsorted

from util import generate_path
from constant.analysis import RESIZE_WIDTH, RESIZE_HEIGHT

def split_text_string(data_path, split_data_directory, string_length=140):
  """.txtファイル内の文字列をn文字ごとに分割
    分割して生成されたデータのヘッダーに分割番号を追加

  Args:
      data_path (str): artificial_satellite/からの相対パス
      split_data_directory (str): artificial_satellite/からの相対パス
      string_length (int): 指定の文字数で分割
      
  Caution:
    改行コードを削除
    分割したデータにヘッダー番号を追加: 
    ヘッダー番号: ファイル番号(分割されたインデックスの値), 16進数, 6文字

  """
  absolute_img_path = generate_path(data_path)
  data = open(absolute_img_path, "r", encoding="utf-8").read()
  if '\n' in data:
    not_new_line_data = data.replace('\n', '')
  else:
    not_new_line_data = data
  splited_data = [not_new_line_data[i:i+string_length] for i in range(0, len(not_new_line_data), string_length)]
  file_name = 1
  for element_index in splited_data:
    header = str(hex(file_name)[2:]).zfill(6)
    packet = f'{generate_path(split_data_directory)}/{file_name}.txt'
    open(packet, "w").write(header + element_index)
    file_name += 1

def combine_string(relative_path):
  """.txtファイル内の文字列同士を結合して1つの.txtファイルを作成

  Args:
    relative_path (str): artificial_satellite/からの相対パス
      e.g.) "/data/aurora_img/*.txt"
  
  Caution:
    0.txtは時刻データのため除外する

    分割されたデータのヘッダーにファイル番号を6文字持つため並び替えた後除外
  """
  img_data = ""
  aurora_data_paths = natsorted(glob.glob(generate_path(relative_path)))
  for aurora_data_path in aurora_data_paths:
    file = open(aurora_data_path, "r")
    aurora_data = file.read()[6:]
    img_data += aurora_data
  return img_data

def convert_img_into_text(relative_img_path, relative_text_path):
  """画像をテキストデータに変換

  Arg:
    relative_img_path (str): artificial_satellite/からの相対パス
  """
  image_path = generate_path(relative_img_path)
  img = cv2.imread(image_path)
  hex_img_data = ""
  flatten_array = img.ravel()
  for element in flatten_array:
    hex_element = format(element, "x").zfill(2)
    hex_img_data += hex_element
  with open(generate_path(relative_text_path), "w") as img_text_file:
    img_text_file.write(hex_img_data)

def restore_img(img_data, restore_relative_path):
  """テキストデータから画像復元

  Args:
    raw_data_relative_path (str): artificial_satellite/からの相対パス
    restore_relative_path (str): artificial_satellite/からの相対パス
    width (int): 横の画素数
    height (int): 縦の画素数
  """
  hex_pixel_array = [img_data[i:i+2] for i in range(0, len(img_data), 2)]
  pixel_array = np.array([])
  for hex_pixel_element in hex_pixel_array:
    pixel_element = int(hex_pixel_element, 16)
    pixel_array = np.append(pixel_array, pixel_element)
  img = pixel_array.reshape(RESIZE_HEIGHT,RESIZE_WIDTH,3)
  cv2.imwrite(generate_path(restore_relative_path), img)
