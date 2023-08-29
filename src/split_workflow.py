from format.uart_communication import receive_command, send_command
from util import shutdown
from analysis.file_generation import convert_img_into_text, split_text_string

def split_workflow():
    send_command("起動完了")
    receive_command("分割指示")
    convert_img_into_text("/img/downlink_img/compressed_img.jpg")
    split_text_string("/data/downlink_data.txt")
    #アップリンクの返答　必要？
    send_command("シャットダウン要求")
    shutdown()