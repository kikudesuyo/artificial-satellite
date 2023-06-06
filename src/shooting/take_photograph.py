import subprocess
import RPi.GPIO as GPIO

from util import generate_path

def take_photo(number_of_shots, interval):
  """撮影

  Args:
      number_of_shots (int): 撮影する枚数
      interval (int): 撮影間隔(ミリ秒) 
  """
  img_path = generate_path("/img/temp/")
  GPIO.setmode (GPIO.BCM)
  GPIO.setup(17,GPIO.OUT)
  for number in range(number_of_shots):
    GPIO.output(17, 1)
    GPIO.output(17, 0)
    shooting = f'raspistill -t {interval} -h 1080 -w 1960 -o {img_path}number{number}.jpg'
    print(shooting)
    ret = subprocess.run(shooting,shell=True, check=True)
    print(ret)
    
take_photo(5, 1000)