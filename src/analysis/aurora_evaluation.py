import cv2
import numpy as np
import re
import glob

from constant import MAX_HSV_RANGE, MIN_HSV_RANGE
from util import generate_path

def get_size(three_dim):
  """要素数を取得"""
  row, column = three_dim.shape[:2]
  size = row * column
  return size

def reshape_array(three_dimension):
  """3次元配列を2次元配列に変更
  
  Arg:
    three_dimension(numpy.ndarray): 3次元配列
  Return:
    two_dimension(numpy.ndarray): 2次元配列
  """
  arrays = get_size(three_dimension)
  two_dimension = three_dimension.reshape(arrays, 3)
  return two_dimension

def erase_noise(absolute_path):
  """ノイズ除去
  
  Arg:
    absolute_path(str): 画像の絶対パス
  Return:
    clear_img(numpy.ndarray): 要素数3の3次元配列
  """
  img = cv2.resize(cv2.imread(absolute_path), dsize=(1960, 1080))
  noize = cv2.imread(generate_path("/img/noise.jpg"))
  clear_img = img - noize
  clear_img[clear_img < 0] = 0 
  return clear_img

def get_aurora_rate(absolute_path):
  """オーロラの画素の割合を取得
  
  Args:
    absolute_path(str):
  Return:
    pixel_rate(float): オーロラ率(0~1の値)
  """
  clear_img = erase_noise(absolute_path)
  img_hsv = cv2.cvtColor(clear_img, cv2.COLOR_BGR2HSV)
  mask_hsv = cv2.inRange(img_hsv, np.array(MIN_HSV_RANGE), np.array(MAX_HSV_RANGE))
  img_hist = np.histogram(np.array(mask_hsv).flatten(), bins=np.arange(256+1))[0]
  not_aurora_pixels = int(img_hist[0])
  aurora_pixels = int(img_hist[255])
  aurora_rate = aurora_pixels/(not_aurora_pixels + aurora_pixels)
  return aurora_rate

def get_aurora_mean(absolute_path, cvtcolor):
  """オーロラである画素の平均値を取得
  
  Args:
    absolute_path(str):
    cvtcolor(int): 色空間の変更 ex.) cv2.COLOR_BGR2HSV

  Return:
  aurora_pixel_mean(numpy.ndarray): 要素数3の一次元配列
  """
  clear_img = erase_noise(absolute_path)
  three_dim = cv2.cvtColor(clear_img, cvtcolor)
  arrays = reshape_array(three_dim)
  aurora_arrays = arrays[np.all(np.array(MAX_HSV_RANGE) >= arrays, axis=1)]
  aurora_arrays = aurora_arrays[np.all(np.array(MIN_HSV_RANGE) <= aurora_arrays, axis=1)]
  aurora_array_elements = len(aurora_arrays)
  aurora_pixel_mean = np.sum(aurora_arrays, axis=0) / aurora_array_elements
  return aurora_pixel_mean

def convert_hsv_to_bgr(hsv_value):
  """HSVからBGRに変換

  Args:
    hsv_value(numpy.ndarray): 1次元配列のHSV値

  Returns:
    bgr_value(numpy.ndarray): 1次元配列のBGR値
  """
  temporary_img = np.array([[hsv_value]])
  bgr_value = cv2.cvtColor(temporary_img.astype(np.uint8), cv2.COLOR_HSV2BGR).flatten()
  return bgr_value

def make_aurora_data_array():
  """オーロラデータをnumpyファイルに格納

  Returns:
    aurora_data_list(numpy.ndarray): [filenumber, オーロラ率, Heu, Saturation, Value]からなる2重配列
  
  Ref:
    配列の中身の型は "numpy.float64"  
  """
  aurora_img_paths = glob.glob(generate_path("/img/test/aurora_consequence/aurora/*.jpg"))
  aurora_data_list = np.empty((0, 5), int)
  for path in aurora_img_paths:
    replace_path = re.sub(r"\\", "/", path)
    file_number = int(re.search(r'_number_(.+).jpg', replace_path).group(1))
    aurora_mean = np.array(get_aurora_mean(path, cv2.COLOR_BGR2HSV))
    aurora_rate = np.array(get_aurora_rate(path))
    aurora_data = np.append(np.array([file_number, aurora_rate]), np.array(aurora_mean))
    aurora_data_list = np.append(aurora_data_list, np.array([aurora_data]), axis=0)
  return aurora_data_list