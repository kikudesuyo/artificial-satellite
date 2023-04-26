import glob
import cv2
import numpy as np
from sklearn.metrics import roc_auc_score
from util import generate_path

def predict_threhold():
  path = generate_path("/predict/")

  aurora = glob.glob(path + "/aurora/*.jpg")
  earth = glob.glob(path + "/earth/*.jpg")

  AUROC_list_all = []
  color_max_list_all = []
  color_min_list_all = []
  for j in range(25):
      color_min = j*10
      AUROC_list = []
      color_max_list = []
      color_min_list = []
      for k in range(18):
          color_max = 255 - k*10
          if color_max <= color_min:
              break
          else:
              color_max_list.append(color_max)
              color_min_list.append(color_min)
              hsv_min = np.array([40, color_min, 0])#多分この値が限界これ以上間を小さくするとオーロラの画像を間違える
              hsv_max = np.array([80, color_max, 255])
              print("hsv_min: {}".format(hsv_min))
              print("hsv_max: {}".format(hsv_max))
              list_max = []#それぞれ画像のの緑色のピクセルの数を収納するリスト
              list_min = []#それぞれ画像の緑色以外のピクセルの数を収納するリスト
              list_hist = []#ヒストグラムを書くためのリスト
              list_percent = []#それぞれの画像の緑色のピクセルと緑色以外のピクセルの比（パーセント）を格納するリスト

              for i in range(len(aurora)):
                  img = cv2.imread(aurora[i])
                  height = img.shape[0]
                  width = img.shape[1]
                  img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                  maskHSV = cv2.inRange(img_HSV,hsv_min,hsv_max)
                  resultHSV = cv2.bitwise_and(img, img, mask = maskHSV)
                  img_hist, img_bins = np.histogram(np.array(maskHSV).flatten(), bins=np.arange(256+1))
                  img_hist_np = np.array(img_hist)
                  list_hist.append(img_hist_np)
                  number_of_max = int(img_hist[255])#緑のピクセルの量
                  list_max.append(number_of_max)
                  number_of_min = int(img_hist[0])#緑以外のピクセルの量
                  list_min.append(number_of_min)
                  percent_green = number_of_max/(number_of_min+number_of_max) #緑とそれ以外のピクセルの割合
                  list_percent.append(percent_green)
              #print(list_max)#それぞれ画像のの緑色のピクセルの数を収納するリストを出力
              #print(list_min)#それぞれ画像の緑色以外のピクセルの数を収納するリストを出力
              #print(list_percent)#それぞれの画像の緑色のピクセルと緑色以外のピクセルの比（パーセント）を格納するリストを出力
              
              list_max_earth = []#それぞれ画像のの緑色のピクセルの数を収納するリスト
              list_min_earth = []#それぞれ画像の緑色以外のピクセルの数を収納するリスト
              list_hist = []#ヒストグラムを書くためのリスト
              list_percent_earth = []#それぞれの画像の緑色のピクセルと緑色以外のピクセルの比（パーセント）を格納するリスト
              for i in range(len(earth)):
                  img = cv2.imread(earth[i])
                  height = img.shape[0]
                  width = img.shape[1]
                  img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                  maskHSV = cv2.inRange(img_HSV,hsv_min,hsv_max)
                  resultHSV = cv2.bitwise_and(img, img, mask = maskHSV)
                  img_hist, img_bins = np.histogram(np.array(maskHSV).flatten(), bins=np.arange(256+1))
                  img_hist_np = np.array(img_hist)
                  list_hist.append(img_hist_np)
                  number_of_max = int(img_hist[255])#緑のピクセルの量
                  list_max_earth.append(number_of_max)
                  number_of_min = int(img_hist[0])#緑以外のピクセルの量
                  list_min_earth.append(number_of_min)
                  percent_green = number_of_max/(number_of_min+number_of_max) #緑とそれ以外のピクセルの割合
                  list_percent_earth.append(percent_green)
              answer = np.concatenate([np.ones(len(aurora)), np.zeros(len(earth))])
              percent_aurora = np.array(list_percent)
              percent_earth = np.array(list_percent_earth)
              percent = np.concatenate([percent_aurora, percent_earth])

              try:
                  AUROC = roc_auc_score(answer, percent)
              except:
                  AUROC = 0
              print("AUROC: {}".format(AUROC))
              AUROC_list.append(AUROC)
      AUROC_list_all.append(AUROC_list)
      color_max_list_all.append(color_max_list)
      color_min_list_all.append(color_min_list)

  max_list = []
  for i in range(len(AUROC_list_all)):
      AUROC_list = AUROC_list_all[i]
      maximum = max(AUROC_list)
      max_list.append(maximum)
  AUROC_max = max(max_list)
  print(AUROC_max)
  max_np = np.array(max_list)
  idx1 = np.where(max_list == AUROC_max)
  idx1 = idx1[0][0]
  print(idx1)
  AUROC_4 = AUROC_list_all[idx1]
  idx2 = np.where(AUROC_4 == AUROC_max[0][0])
  idx2 = idx2[0][0]
  print(idx2)
  print(color_min_list_all[idx1][idx2])
  print(color_max_list_all[idx1][idx2])