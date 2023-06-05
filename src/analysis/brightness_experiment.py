import glob, re, cv2, csv

from constant import AURORA_THREHOLD
from  util import generate_path, delete_files, get_current_time
from analysis.aurora_evaluation import AuroraAnalysis

def distribute(absolute_path, filename):
  """実験用の関数 実装と異なるので注意すること。

  Args:
      absolute_path (_type_): _description_
      filename (_type_): _description_
  """
  instance = AuroraAnalysis()
  clear_img = instance.erase_noise(absolute_path)
  aurora_rate = instance.get_aurora_rate(absolute_path)
  current_time = get_current_time()
  filename = re.search(r'aurora_test(.+).jpg', absolute_path).group(1)[1:]
  if aurora_rate >= AURORA_THREHOLD:
    aurora_img_path = generate_path("/img/test/aurora_consequence/aurora/time_" + str(current_time) + "_number_" + str(filename) + ".jpg")
    cv2.imwrite(aurora_img_path, clear_img)
  else:
    not_aurora_img_path = generate_path("/img/test/aurora_consequence/unaurora/time_" + str(current_time) + "_number_" +str(filename) + ".jpg")
    cv2.imwrite(not_aurora_img_path, clear_img)
    
# ファイル振り分け
delete_files("/data/packet")
delete_files("/img/test/aurora_consequence/aurora")
delete_files("/img/test/aurora_consequence/unaurora")
img_paths = glob.glob(generate_path("/img/aurora_test/*.jpg"))
filenumber = 1
for img_path in img_paths:
  distribute(img_path, filenumber)
  filenumber += 1

instance = AuroraAnalysis()
#データ解析
with open(generate_path("/data/result.csv"), "a") as f:
  aurora_img_paths = glob.glob(generate_path("/img/test/aurora_consequence/aurora/*.jpg"))
  for aurora_img_path in aurora_img_paths:
    aurora_rate = str(round(instance.get_aurora_rate((aurora_img_path)), 2))
    aurora_mean = instance.get_aurora_mean(aurora_img_path, cv2.COLOR_BGR2HSV)
    raw_hue, raw_saturation, raw_value = aurora_mean
    hue = str(int(raw_hue))
    saturation = str(int(raw_saturation))
    value = str(int(raw_value))
    filename = re.search(r'number_(.+).jpg', aurora_img_path).group(1)
    writer = csv.writer(f)
    writer.writerow([filename, aurora_rate, hue, saturation, value])