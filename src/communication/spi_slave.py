import Rpi.GPIO as GPIO

from constant import MISO, SCLK, MOSI
from communication.shape_up import get_aurora_data, get_binary_data
def init():
  GPIO.setwarnings(False)
  GPIO.cleanup()
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(MISO, GPIO.OUT)
  GPIO.setup(MOSI, GPIO.OUT)
  GPIO.setup(SCLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  print("Done")
  
def send_data(downlink_data):
  """送信関数

  Args:
    downlink_data (str): 2進数の文字列
  
  Overview:
    SCLKの値が0に下がったタイミングでデータを送信
  
  Caution:
    MASTERがSCLKの値を読み込めないためMOSIを実験的に使用する。
    本番環境では削除する。
  """
  flag = 1
  for bit_data in downlink_data:
    if GPIO.input(SCLK) == 1:
      flag = 1
    else:
      while True:
        if GPIO.input(SCLK) == 0:
          GPIO.output(MOSI, True)
          break
    if GPIO.input(SCLK) == 0 and flag == 1:
      GPIO.output(MISO, int(bit_data))
      GPIO.output(MOSI, False)
        
init()
aurora_data = get_aurora_data("/data/aurora_data/*")
downlink_data = get_binary_data(aurora_data)

# send_data("143")
