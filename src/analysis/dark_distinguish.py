import cv2
import numpy as np
from util import generate_path
from constant import AURORA_THREHOLD
 
def divide_aurora_image():
  path = generate_path("/img/")
  img = cv2.imread(path + "/temp/compression/test.jpg")
  dark_img = []
  # 恐らく縦の長さが1の画像を用意している。rgb値は全て0(黒の画像)
  # dark_img = cv2.imread(img + "temp/compression/test.jpg")
  hsv_min = np.array([40, 60, 0])
  hsv_max = np.array([60, 245, 255])
  # print(type(dark_img))
  for i in range(len(img)):
    # print(img[i])
    img_row = img[i]
    reduce_noize = img - dark_img
    reduce_noize[reduce_noize<0] = 0 
    img_HSV = cv2.cvtColor(reduce_noize, cv2.COLOR_BGR2HSV)
    maskHSV = cv2.inRange(img_HSV,hsv_min,hsv_max)
    resultHSV = cv2.bitwise_and(reduce_noize, reduce_noize, mask = maskHSV)
    img_hist, img_bins = np.histogram(np.array(maskHSV).flatten(), bins=np.arange(256+1))
    number_of_max = int(img_hist[255])
    number_of_min = int(img_hist[0])
    percent_green = number_of_max/number_of_min
    if percent_green >= AURORA_THREHOLD:
        aurora_img = img + "/aurora/number/"+ str(i) + ".jpg"
        cv2.imwrite(aurora_img, reduce_noize)
    else:
        not_aurora_img = img + "/unaurora/number/" + str(i) + ".jpg"
        cv2.imwrite(not_aurora_img, reduce_noize)