import cv2
from util import generate_path

def compress_img(minify_img_path, compression_ratio):
  """画像の圧縮
  
  Arg:
    minify_img_path(str): artificial_satellite/からの相対パス
    compression_ratio(int): 縦横それぞれを圧縮
  """
  img = cv2.imread(generate_path(minify_img_path))
  height, width = img.shape[:2]
  resized_img = cv2.resize(img,(round(width/compression_ratio), round(height/compression_ratio)))
  compressed_path = generate_path("/img/downlink_img/compressed_img.jpg")
  cv2.imwrite(compressed_path, resized_img)