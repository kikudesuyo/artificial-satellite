import Rpi.GPIO as GPIO
import time

from constant import SPI_MOSI, SPI_SCLK

def init():
  GPIO.setwarnings(False)
  GPIO.cleanup()
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(SPI_MOSI, GPIO.IN)
  GPIO.setup(SPI_SCLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  print("Done")

init()
slave_binary_data = ""
while True:
  if GPIO.input(SPI_SCLK) == 1:
    bit_data = GPIO.input(SPI_MOSI)
    print(bit_data)
    slave_binary_data += str(bit_data)
    time.sleep(1)
    if GPIO.input(SPI_SCLK) == 0:
      break
slave_binary_data = "1" + slave_binary_data[1:]
recieved_data = int(slave_binary_data)
print("recieved data is :" + str(recieved_data))
