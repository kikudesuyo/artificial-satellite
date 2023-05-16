
import glob
import cv2
import numpy as np
from constant import MIN_HSV_RANGE, MAX_HSV_RANGE, IMAGE_SIZE
import time
from util import generate_path

def rate_a(img_path):
  img = cv2.imread(img_path)
  noise_img = cv2.imread(generate_path("/img/noise.jpg"))
  clear_img = img - noise_img
  clear_img[clear_img < 0] = 0
  img_hsv = cv2.cvtColor(clear_img, cv2.COLOR_BGR2HSV)
  mask_hsv = cv2.inRange(img_hsv, np.array(MIN_HSV_RANGE), np.array(MAX_HSV_RANGE))
  img_hist = np.histogram(np.array(mask_hsv).flatten(), bins=np.arange(256+1))[0]
  not_aurora_pixels = int(img_hist[0])
  aurora_pixels = int(img_hist[255])
  aurora_rate = aurora_pixels/(not_aurora_pixels + aurora_pixels)
  return aurora_rate

def rate_b(img_path):
  img = cv2.imread(img_path)
  noise_img = cv2.imread(generate_path("/img/noise.jpg"))
  clear_img = img - noise_img
  clear_img[clear_img < 0] = 0
  img_hsv = cv2.cvtColor(clear_img, cv2.COLOR_BGR2HSV)
  mask_hsv = cv2.inRange(img_hsv, np.array(MIN_HSV_RANGE), np.array(MAX_HSV_RANGE))
  img_hist = np.histogram(np.array(mask_hsv).flatten(), bins=np.arange(256+1))[0]
  aurora_pixels = int(img_hist[255])
  aurora_rate = aurora_pixels/ IMAGE_SIZE
  return aurora_rate

  
  
  
img_paths = glob.glob(generate_path("/img/aurora/*"))

for i in range(20):
  start = time.perf_counter()
  for img_path in img_paths:
    rate = rate_a(img_path)
    # print(rate)
  end = time.perf_counter()
  a = end - start
  print("a" + str(a))
    
  start = time.perf_counter()
  for img_path in img_paths:
    rate = rate_b(img_path)
    # print()
  end = time.perf_counter()
  b = end - start
  print("b" + str(b))
  print("shortened time is:" + str(a - b))


def change_color_space(self, img_path):
  clear_img = self.erase_noise(img_path)
  img_hsv = cv2.cvtclor(clear_img, cv2.COLOR_BGR2HSV)
  return img_hsv