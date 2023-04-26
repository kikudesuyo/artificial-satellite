import cv2, glob, time

from analysis.aurora_index import get_aurora_mean, get_aurora_rate
from analysis.resize import compress_img
from analysis.predict_threhold import predict_threhold
from analysis.split_text import get_packet
from  util import generate_path
# get_packet()
# predict_threhold()
# from analysis.dark_distinguish import divide_aurora_image

# start = time.perf_counter()
# print("start")
# path = generate_path("/img/aurora/*.jpg")
# imgs = glob.glob(path)
# for img in imgs:
#   print(get_aurora_mean(img, cv2.COLOR_BGR2HSV))

# end = time.perf_counter()
# handle_time = end - start
# print("end")
# print("handle time is :"+ str(handle_time))