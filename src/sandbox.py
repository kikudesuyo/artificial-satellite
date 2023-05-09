import glob, time
import re
import cv2

from  util import delete_files
from analysis.aurora_distinguish import distribute_aurora_img
from analysis.aurora_evaluation import make_aurora_data_array, get_aurora_mean, get_aurora_rate


start = time.perf_counter()
print("start")
delete_files("/data/packet")
delete_files("/img/test/aurora_consequence/aurora")
delete_files("/img/test/aurora_consequence/unaurora")
end = time.perf_counter()
print("end")
print("handle time is:" + str(end - start))