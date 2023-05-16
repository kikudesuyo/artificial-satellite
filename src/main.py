from  util import generate_path, delete_files
from analysis.aurora_evaluation import make_aurora_data_array

def main():
  # 初期化
  delete_files("/data/packet")
  #データ解析
  aurora_data_list = make_aurora_data_array("/img/aurora/*.jpg")
  # テキストファイルに出力
  for aurora_data in aurora_data_list:
    raw_file_number, raw_aurora_rate, raw_hue, raw_saturation, raw_value = aurora_data
    file_number = str(int(raw_file_number))
    aurora_rate = str(round(raw_aurora_rate, 2))
    hue = str(int(raw_hue))
    saturation = str(int(raw_saturation))
    value = str(int(raw_value))
    text_file = open(generate_path("/data/packet/" + file_number + ".txt"), "w")
    text_file.write(file_number + aurora_rate + hue + saturation + value)
    text_file.close()

# if __name__== '__main__':
main()