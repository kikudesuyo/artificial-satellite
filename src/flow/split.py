import os
from util import generate_path, delete_files
from helper.file_operation import output_raspi_status
from analysis.file_generation import convert_img_into_text, split_text_string
from constant.status import SPLIT_INTERRUPTION, OTHERS_COMPLETION

def split_flow():
    output_raspi_status(SPLIT_INTERRUPTION)
    delete_files("/data/aurora_img")
    downlink_img = os.listdir(generate_path("/img/downlink_img"))[0]
    convert_img_into_text(f"/img/downlink_img/{downlink_img}", "/data/downlink_data.txt")
    split_text_string("/data/downlink_data.txt", "/data/aurora_img")
    #delete_files("/img/downlink_img")
    output_raspi_status(OTHERS_COMPLETION)