import cv2
import numpy as np
import re
import glob

from constant import AURORA_THREHOLD, MAX_HSV_RANGE, MIN_HSV_RANGE, IMAGE_SIZE
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

  def get_aurora_rate(self, img_path):
    """オーロラの画素の割合を取得
    
    Args:
      clear_img(numpy.ndarray):
    Return:
      pixel_rate(float): オーロラ率(0~1の値)
    """
    img_hsv = self.change_color_space(img_path)
    mask_hsv = cv2.inRange(img_hsv, np.array(MIN_HSV_RANGE), np.array(MAX_HSV_RANGE))
    img_hist = np.histogram(np.array(mask_hsv).flatten(), bins=np.arange(256+1))[0]
    aurora_pixels = int(img_hist[255])
    aurora_rate = aurora_pixels/ IMAGE_SIZE
    return aurora_rate

  def get_aurora_mean(self, img_path):
    """オーロラである画素の平均値を取得
    
    Args:
      clear_img(numpy.ndarray):
      cvtcolor(int): 色空間の変更 ex.) cv2.COLOR_BGR2HSV

    Return:
    aurora_pixel_mean(numpy.ndarray): 要素数3の一次元配列
    """
    three_dim = self.change_color_space(img_path)
    arrays = self.reshape_array(three_dim)
    aurora_arrays = arrays[np.all((np.array(MAX_HSV_RANGE) >= arrays) & (arrays >= np.array(MIN_HSV_RANGE)), axis=1)]
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

def make_aurora_data_array(img_path):
  """オーロラデータをnumpyファイルに格納

  Arg:
    img_path(str): artificial_satellite/からの相対パス

  Returns:
    aurora_data_list(numpy.ndarray): [filenumber, オーロラ率, Heu, Saturation, Value]からなる2重配列
  
  Ref:
    配列の中身の型は "numpy.float64"
  """
  analysis = AuroraAnalysis()
  aurora_data_list = np.empty((0, 5), int)
  img_paths = glob.glob(generate_path(img_path))
  for img_path in img_paths:
    aurora_rate = analysis.get_aurora_rate(img_path)
    if aurora_rate < AURORA_THREHOLD:
      continue
    replace_path = re.sub(r"\\", "/", img_path)
    # file_number → shooting_time
    # 撮影時刻はファイル名から取得する(numpyに格納するため、int型にしなければいけない)
    # shooting_time = re.search(r'time_(.+)_number', ).group(1)
    file_number = int(re.search(r'test(.+).jpg', replace_path).group(1))
    aurora_mean = np.array(analysis.get_aurora_mean(img_path))
    aurora_data = np.append(np.array([file_number, aurora_rate]), np.array(aurora_mean))
    aurora_data_list = np.append(aurora_data_list, np.array([aurora_data]), axis=0)
  return aurora_data_list