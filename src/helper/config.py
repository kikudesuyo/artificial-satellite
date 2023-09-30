import re
from util import generate_path

def change_elec_power(clock_freq):
  with open(generate_path("/helper/saved_config.txt"), "r") as config_file:
    config_contents = config_file.read()
  modified_contents = re.sub(r"(?<!#)arm_freq=[0-9]{0,10}", "arm_freq="+clock_freq, config_contents)
  with open("/boot/config.txt", "w") as exe_config_file:
    exe_config_file.write(modified_contents)
  