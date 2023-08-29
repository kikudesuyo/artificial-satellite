from util import shutdown, set_date_on_raspi, delete_files
from shooting.take_photograph import take_photo
from analysis.main import main as analysis_main
from analysis.file_generation import convert_img_into_text, split_text_string
from downlink.main import main as communication_main
from downlink.shape_up import get_aurora_data, get_splited_data
from format.uart_communication import send_command, receive_command
from util import generate_path

def execute():
  command = receive_command(15)
  if command == "オーロラ撮影":
    time_data = receive_command(15)
    with open(generate_path("/data/satellite_time.txt"), "w") as file:
      file.write(time_data)
    set_date_on_raspi("0001/01/01 00:00:00")
    take_photo(shooting_times=10, interval_msec=2000)
    send_command("撮影終了")
  elif command == "画像解析":
    analysis_main()
    delete_files("/img/shooting_img/*")
    send_command("解析終了")
  elif command == "画像分割":
    delete_files("/data/aurora_img")
    convert_img_into_text("/img/downlink_img/compressed_img.jpg")
    split_text_string("/data/downlink_data.txt")
    send_command("分割終了")
  elif command == "ダウンリンク":
    downlink_command = receive_command(15)
    if downlink_command == "オーロラデータダウンリンク":
      sending_data = get_aurora_data("/data/aurora_data/*.txt")
    elif downlink_command == "画像分割ダウンリンク":
      #indexの指定をどうするかを考える(オーロラデータは行わない予定なのでそこに注意)
      sending_data = get_splited_data("/data/aurora_img/*.txt")
    communication_main(sending_data)
    send_command("通信終了")
    delete_files("/data/aurora_data")
  shutdown()