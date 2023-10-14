import os
import re

from util import generate_path, delete_files
from helper.file_operation import output_raspi_status, write_to_file
from analysis.file_generation import convert_img_into_text, split_text_string
from constant.status import SPLIT_INTERRUPTION, OTHERS_COMPLETION

def split_flow():
    output_raspi_status(SPLIT_INTERRUPTION)
    delete_files("/data/aurora_img")
    downlink_img = os.listdir(generate_path("/img/downlink_img"))[0]
    relative_img_path = f"/img/downlink_img/{downlink_img}"
    convert_img_into_text(relative_img_path, "/data/downlink_data.txt")
    split_text_string("/data/downlink_data.txt", "/data/aurora_img")
    shooting_time = re.sub(r'\D', '', generate_path(relative_img_path))
    write_to_file(shooting_time, "/data/aurora_img/0.txt")
    delete_files("/img/downlink_img")
    output_raspi_status(OTHERS_COMPLETION)