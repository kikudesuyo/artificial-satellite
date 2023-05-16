import glob, cv2, time
import numpy as np
from constant import MAX_HSV_RANGE, MIN_HSV_RANGE, IMAGE_SIZE
from util  import generate_path

for i in range(10):
  after_start = time.perf_counter()
  img_paths = glob.glob(generate_path('/img/aurora/*'))
  for img_path in img_paths:
    img = cv2.imread(img_path)
    noise_img = cv2.imread(generate_path('/img/noise.jpg'))
    clear_img = img - noise_img
    clear_img[clear_img < 0] = 0 
    img_hsv = cv2.cvtColor(clear_img, cv2.COLOR_BGR2HSV)
    arrays = img_hsv.reshape(IMAGE_SIZE, 3)
    aurora_arrays = arrays[np.all((np.array(MAX_HSV_RANGE) >= arrays) & (arrays >= np.array(MIN_HSV_RANGE)), axis=1)]
    aurora_array_elements = len(aurora_arrays)
    aurora_pixel_mean = np.sum(aurora_arrays, axis=0) / aurora_array_elements
    # print(aurora_pixel_mean)
  after_end = time.perf_counter()
  print("after" + str(after_end - after_start))
  
  
  before_start = time.perf_counter()
  img_paths = glob.glob(generate_path('/img/aurora/*'))
  for img_path in img_paths:
    img = cv2.imread(img_path)
    noise_img = cv2.imread(generate_path('/img/noise.jpg'))
    clear_img = img - noise_img
    clear_img[clear_img < 0] = 0 
    img_hsv = cv2.cvtColor(clear_img, cv2.COLOR_BGR2HSV)
    arrays = img_hsv.reshape(IMAGE_SIZE, 3)
    aurora_arrays = arrays[np.all(np.array(MAX_HSV_RANGE) >= arrays, axis=1)]
    aurora_arrays = aurora_arrays[np.all(np.array(MIN_HSV_RANGE) <= aurora_arrays, axis=1)]
    aurora_array_elements = len(aurora_arrays)
    aurora_pixel_mean = np.sum(aurora_arrays, axis=0) / aurora_array_elements
    # print(aurora_pixel_mean)
  before_end = time.perf_counter()
  print("before" + str(before_end - before_start)) 