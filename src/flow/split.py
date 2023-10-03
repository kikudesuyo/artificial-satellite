from util import delete_files
from helper.file_operation import output_raspi_status
from analysis.file_generation import convert_img_into_text, split_text_string
from constant.status import SPLIT_INTERRUPTION, OTHERS_COMPLETION

def split_flow():
    output_raspi_status(SPLIT_INTERRUPTION)
    delete_files("/data/aurora_img")
    convert_img_into_text("/img/downlink_img/compressed_img.jpg")
    split_text_string("/data/downlink_data.txt")
    #delete_files("/img/downlink_img")
    output_raspi_status(OTHERS_COMPLETION)