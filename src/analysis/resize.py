import cv2
from util import generate_path

def compress_img(img_path, compression_ratio):
  """画像の圧縮
  arg:
   img_path(str): img/からのpath ex.) /img/aurora/test.jpg
  compression_ratio(int): 縦横それぞれを圧縮
  """
  img = cv2.imread(img_path)
  print(img)
  height, width = img.shape[:2]
  resized_img = cv2.resize(img,(round(width/compression_ratio), round(height/compression_ratio)))
  compressed_path = generate_path("/img/temp/compression/test1.jpg")
  cv2.imwrite(compressed_path, resized_img)
