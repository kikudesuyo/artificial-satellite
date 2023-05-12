import glob
import time

from  util import generate_path, delete_files
from analysis.aurora_distinguish import distribute_aurora_img
from analysis.aurora_evaluation import make_aurora_data_array
# ファイル振り分け
start = time.perf_counter()
print("start")
delete_files("/data/packet")
delete_files("/img/test/aurora_consequence/aurora")
delete_files("/img/test/aurora_consequence/unaurora")
img_paths = glob.glob(generate_path("/predict/machine_learning/aurora/*.jpg"))
filenumber = 1
for img_path in img_paths:
  distribute_aurora_img(img_path, filenumber)
  filenumber += 1
end = time.perf_counter()
print("end")
print("handle time is:" + str(end - start))

#データ解析
# start = time.perf_counter()

print("start")
# テキストファイルに出力
aurora_data_list = make_aurora_data_array()
for aurora_data in aurora_data_list:
  raw_file_number, raw_aurora_rate, raw_hue, raw_saturation, raw_value = aurora_data
  file_number = str(int(raw_file_number))
  aurora_rate = str(round(raw_aurora_rate, 2))
  hue = str(int(raw_hue))
  saturation = str(int(raw_saturation))
  value = str(int(raw_value))
  # ファイル番号からファイルのパスを取得
  #パスから時刻取得
  # current_time = re.search(r'time_(.+)_number', ).group(1)
  print(file_number + aurora_rate + hue + saturation + value)
  text_file = open(generate_path("/data/packet/" + file_number + ".txt"), "w")
  text_file.write(file_number + aurora_rate + hue + saturation + value)
  text_file.close()

end = time.perf_counter()
print("end")
print("handle time is:" + str(end - start))