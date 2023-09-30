from util import delete_files
from analysis.file_generation import convert_img_into_text, split_text_string

def split_flow():
    delete_files("/data/aurora_img")
    convert_img_into_text("/img/downlink_img/compressed_img.jpg")
    split_text_string("/data/downlink_data.txt")
    #delete_files("/img/downlink_img")
    #アップリンクの返答　必要？