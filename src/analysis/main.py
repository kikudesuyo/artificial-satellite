from util import generate_path, delete_files, convert_datetime_to_hex_seconds
from analysis.aurora_evaluation import make_aurora_data

def main():
  # 初期化 本番環境では使用しない
  delete_files("/data/aurora_data")
  #データ解析
  aurora_data_list = make_aurora_data("/img/aurora/*.jpg")
  #.txtにオーロラデータ出力
  for aurora_data in aurora_data_list:
    raw_date_time, raw_aurora_rate, raw_hue, raw_saturation, raw_value = aurora_data
    date_time = str(int(raw_date_time)).zfill(8)
    hex_date_time = convert_datetime_to_hex_seconds(date_time)
    hex_aurora_percentage = format(int(round(raw_aurora_rate, 2) *100), "x").zfill(2)
    hex_hue = format(int(raw_hue), "x").zfill(2)
    hex_saturation = format(int(raw_saturation), "x").zfill(2)
    hex_value = format(int(raw_value), "x").zfill(2)
    with open(generate_path(f'/data/aurora_data/{date_time}.txt'), "w") as text_file:
      text_file.write(hex_date_time + hex_aurora_percentage + hex_hue + hex_saturation + hex_value)
