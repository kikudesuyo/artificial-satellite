import cv2
import re

from util import generate_path, get_current_time
from constant import AURORA_THREHOLD
from analysis.aurora_evaluation import erase_noise, get_aurora_rate

def distribute_aurora_img(absolute_path, filename):
  """画像にオーロラが映っているかどうかを振り分け

  Args:
    absolute_path (str):
    filename (int): 画像の番号を指定
  """
  clear_img = erase_noise(absolute_path)
  aurora_rate = get_aurora_rate(absolute_path)
  current_time = get_current_time()
  if aurora_rate >= AURORA_THREHOLD:
    aurora_img_path = generate_path("/img/test/aurora_consequence/aurora/time_" + str(current_time) + "_number_" + str(filename) + ".jpg")
    cv2.imwrite(aurora_img_path, clear_img)
  else:
    not_aurora_img_path = generate_path("/img/test/aurora_consequence/unaurora/time_" + str(current_time) + "_number_" +str(filename) + ".jpg")
    cv2.imwrite(not_aurora_img_path, clear_img)