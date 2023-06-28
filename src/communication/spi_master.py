import Rpi.GPIO as GPIO
import time
#本番で使用するpinはMISOとSCLK MOSIは実験用に使用
from constant import MISO, SCLK, MOSI

def init():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(MISO, GPIO.IN)
  GPIO.setup(MOSI, GPIO.IN)
  GPIO.setup(SCLK, GPIO.OUT, initial=GPIO.HIGH) 
  pwm = GPIO.PWM(SCLK, 4800)
  pwm.start(50)
  print("Done")

def receive_data():
  """受信関数
  
  Overview:
    MOSIの値が1であれば読み込み、0であれば1になるまで待機
    値が変化しなかったら実行を中止
  
  """
  binary_data = ""
  quit_flag = False
  while True:
    if GPIO.input(MOSI) == True:
      bit_data = GPIO.input(MISO)
      binary_data += bit_data
    else:
      start = time.strftime()
      while GPIO.input(MOSI) == False:
        end = time.strftime()
        execute_time = end - start
        if execute_time > 10:
          quit_flag = True
          break
    if quit_flag:
      break
  return binary_data

binary_data = receive_data()
# binary_data = "1" + binary_data[1:]
# recieved_data = int(binary_data)
print("recieved data is :" + str(binary_data))