import time
from util import generate_path, delete_files
from analysis.aurora_evaluation import make_aurora_data

def main():
  # 初期化 本番環境では使用しない
  delete_files("/data/aurora_data")
  #データ解析
  #Caution: 撮影した画像を解析
  aurora_data_list = make_aurora_data("/img/shooting_img/test1.jpg")
  #.txtにオーロラデータ出力
  file_number = 1
  for aurora_data in aurora_data_list:
    raw_date_time, raw_aurora_rate, raw_hue, raw_saturation, raw_value = aurora_data
    date_time = hex(int(raw_date_time))[2:].zfill(8)
    hex_aurora_percentage = format(int(round(raw_aurora_rate, 2) *100), "x").zfill(2)
    hex_hue = format(int(raw_hue), "x").zfill(2)
    hex_saturation = format(int(raw_saturation), "x").zfill(2)
    hex_value = format(int(raw_value), "x").zfill(2)
    with open(generate_path(f'/data/aurora_data/{file_number}.txt'), "w") as text_file:
      text_file.write(date_time + hex_aurora_percentage + hex_hue + hex_saturation + hex_value)
    file_number += 1



# start = time.perf_counter()

# count = 0
# while count < 10:
#   main()
#   count += 1
# time.sleep(1)
# end = time.perf_counter()

# print(end-start)


from util import delete_particular_file

delete_particular_file(generate_path("/data/merged_aurora_data/a.txt"))