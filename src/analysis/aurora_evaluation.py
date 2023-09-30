import cv2
import numpy as np
import re
import glob
from natsort import natsorted

from constant.analysis import AURORA_THREHOLD, MAX_HSV_RANGE, MIN_HSV_RANGE, IMAGE_SIZE
from util import generate_path

class AuroraAnalysis():
  
  def __init__(self):
    self.noise_img = cv2.imread(generate_path("/img/noise.jpg"))

  def reshape_array(self, three_dimension):
    """3次元配列を2次元配列に変更
    
    Arg:
      three_dimension(numpy.ndarray): 3次元配列
    Return:
      two_dimension(numpy.ndarray): 2次元配列
    """
    arrays = IMAGE_SIZE
    two_dimension = three_dimension.reshape(arrays, 3)
    return two_dimension

  def erase_noise(self, img_path):
    """ノイズ除去
    
    Arg:
      img_path(str): 画像の絶対パス
    Return:
      clear_img(numpy.ndarray): 要素数3の3次元配列
    """
    img = cv2.imread(img_path)
    clear_img = img - self.noise_img
    clear_img[clear_img < 0] = 0 
    return clear_img
  
  def change_color_space(self, img_path):
    clear_img = self.erase_noise(img_path)
    img_hsv = cv2.cvtColor(clear_img, cv2.COLOR_BGR2HSV)
    return img_hsv

  def calculate_aurora_rate(self, img_hsv):
    """オーロラの画素の割合を取得
    
    Args:
      clear_img(numpy.ndarray):
    Return:
      pixel_rate(float): オーロラ率(0~1の値)
    """
    mask_hsv = cv2.inRange(img_hsv, np.array(MIN_HSV_RANGE), np.array(MAX_HSV_RANGE))
    img_hist = np.histogram(np.array(mask_hsv).flatten(), bins=np.arange(256+1))[0]
    aurora_pixels = int(img_hist[255])
    aurora_rate = aurora_pixels / IMAGE_SIZE
    return aurora_rate

  def calculate_aurora_mean(self, img_hsv):
    """オーロラである画素の平均値を取得
    
    Args:
      clear_img(numpy.ndarray):
      cvtcolor(int): 色空間の変更 ex.) cv2.COLOR_BGR2HSV

    Return:
    aurora_pixel_mean(numpy.ndarray): 要素数3の一次元配列
    """
    arrays = self.reshape_array(img_hsv)
    aurora_arrays = arrays[np.all((np.array(MAX_HSV_RANGE) >= arrays) & (arrays >= np.array(MIN_HSV_RANGE)), axis=1)]
    aurora_pixel_mean = np.mean(aurora_arrays, axis=0)
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

def make_aurora_data(img_relative_path):
  """オーロラデータをnumpyに格納

  Arg:
    img_relative_path(str): artificial_satellite/からの相対パス

  Returns:
    aurora_data_list(numpy.ndarray): [filenumber, オーロラ率, Heu, Saturation, Value]からなる2重配列
  
  Ref:
    配列の中身の型は "numpy.float64"
  """
  analysis = AuroraAnalysis()
  aurora_data_list = np.empty((0, 5), int)
  img_paths = natsorted(glob.glob(generate_path(img_relative_path)))
  for img_path in img_paths:
    img_hsv = analysis.change_color_space(img_path)
    aurora_rate = analysis.calculate_aurora_rate(img_hsv)
    if aurora_rate < AURORA_THREHOLD:
      continue
    shooting_time = int(re.sub(r'\D', '', img_path))
    aurora_mean = np.array(analysis.calculate_aurora_mean(img_hsv))
    aurora_data = np.concatenate((np.array([shooting_time, aurora_rate]), aurora_mean))
    aurora_data_list = np.append(aurora_data_list, np.array([aurora_data]), axis=0)
  return aurora_data_list

#a