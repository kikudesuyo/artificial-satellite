import RPi.GPIO as GPIO

from constant import MISO, SCLK, MOSI

class SpiCommunication():
  def __init__(self):
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MISO, GPIO.OUT)
    #GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(SCLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Done")
    
  def send_data(self, downlink_data):
    """送信関数

    Args:
      downlink_data (str): 2進数の文字列
    
    Overview:
      SCLKの値が0に下がったタイミングでデータを送信
    
    Caution:
      MASTERがSCLKの値を読み込めないためMOSIを実験的に使用する。
      本番環境ではMOSIは全て削除する。
    """
    for bit_data in downlink_data:
      while True:
        if GPIO.input(SCLK) == 1:
          break
      while True:
        if GPIO.input(SCLK) == 0:
          GPIO.output(MISO, int(bit_data))
          break
      # if GPIO.input(SCLK) == 0 and flag == 1:
      #   GPIO.output(MISO, int(bit_data))
      #   GPIO.output(MOSI, False)