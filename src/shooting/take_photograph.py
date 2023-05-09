import subprocess
import RPi.GPIO as GPIO

from util import generate_path

def take_photo(number_of_shots):
  img_path = generate_path("/img/temp/")
  GPIO.setmode (GPIO.BCM)
  GPIO.setup(17,GPIO.OUT)
  for number in range(number_of_shots):
    GPIO.output(17, 1)
    GPIO.output(17, 0)
    shooting = f'raspistill -t 10 -h 1080 -w 1960 -o {img_path}number{number}.jpg'
    print(shooting)
    ret = subprocess.run(shooting,shell=True, check=True)
    print(ret)