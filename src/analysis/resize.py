import cv2
from util import generate_path
  
def compress_img(minify_img_path, width=1960, height=1080):
  """画像の圧縮
  
  Arg:
    minify_img_path(str): artificial_satellite/からの相対パス
    width, height (int): pixel数
  """
  img = cv2.imread(generate_path(minify_img_path))
  resized_img = cv2.resize(img, (width, height))
  compressed_path = generate_path("/img/downlink_img/compressed_img.jpg")
  cv2.imwrite(compressed_path, resized_img)