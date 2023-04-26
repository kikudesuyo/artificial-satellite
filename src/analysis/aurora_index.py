import cv2
import numpy as np
from constant import MAX_HSV_RANGE, MIN_HSV_RANGE

def img_to_array(absolute_path):
  """画像をnumpy.ndarrayに変更
  
  Arg:
    absolute_path(str):
  Return:
    img_array(numpy.ndarray)
  """
  array = cv2.imread(absolute_path)
  return array

def change_color_space(absolute_path, cvtcolor):
  """指定の色空間を取得
  
  Args:
    absolute_path(str):
    cvtcolor(int): 色空間の変更 ex.) cv2.COLOR_BGR2HSV
  Return:
    pixel_array(numpy.ndarray):
  """
  array = img_to_array(absolute_path)
  color_space = cv2.cvtColor(array, cvtcolor)
  return color_space

def get_element_count(three_dim):
  """要素数を取得"""
  height, width = three_dim.shape[:2]
  size = height * width
  return size

def reshape_array(three_dimension):
  """3次元配列を2次元配列に変更
  
  Arg:
    three_dimension(numpy.ndarray): 3次元配列
  Return:
    two_dimension(numpy.ndarray):
  """
  arrays = get_element_count(three_dimension)
  two_dimension = three_dimension.reshape(arrays, 3)
  return two_dimension

def is_aurora_pixel(pixel):
  """オーロラの画素を満たす画素か判定
  
  Arg:
    pixel (numpy.ndarray): 要素数3の一次元配列
  Return:
    all() (bool):
  """
  min_hsv_range = (MIN_HSV_RANGE >= pixel).all()
  max_hsv_range = (MAX_HSV_RANGE <= pixel).all()
  return all([min_hsv_range, max_hsv_range])

def get_aurora_rate(absolute_path, cvtcolor):
  """オーロラの画素の割合を取得
  
  Args:
    absolute_path(str):
    cvtcolor(int): 色空間の変更 ex.) cv2.COLOR_BGR2HSV
  Return:
    pixel_rate(float): オーロラ率(0~1の値)
  """
  three_dim = change_color_space(absolute_path, cvtcolor)
  pixel_arrays = reshape_array(three_dim)
  particular_pixels = 0
  for pixel in pixel_arrays:
    if is_aurora_pixel(pixel):
      particular_pixels += 1
  pixel_rate = particular_pixels / get_element_count(three_dim)
  return pixel_rate  

def get_aurora_mean(absolute_path, cvtcolor):
  """オーロラである画素の平均値を取得
  
  Args:
    absolute_path(str):
    cvtcolor(int): 色空間の変更 ex.) cv2.COLOR_BGR2HSV

  Return:
  aurora_pixel_mean(numpy.ndarray): 要素数3の一次元配列
  """
  three_dim = change_color_space(absolute_path, cvtcolor)
  arrays = reshape_array(three_dim)
  aurora_arrays = np.empty((0, 3), dtype=int)
  for pixel in arrays:
    if is_aurora_pixel(pixel):
      aurora_arrays = np.append(aurora_arrays, np.array([pixel]), axis=0)
  aurora_pixel_mean = np.mean(aurora_arrays, axis=0).tolist()
  return aurora_pixel_mean