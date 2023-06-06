import Rpi.GPIO as GPIO
import time

from constant import SPI_MOSI, SPI_SCLK

def init():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(SPI_MOSI, GPIO.OUT)
  GPIO.setup(SPI_SCLK, GPIO.OUT, initial=GPIO.HIGH)
  print("Done")

def send_data(int_data):
  binary_digits = len(format(int_data, '#b')[2:])
  for index in range(binary_digits):
    binary = (int_data >> (binary_digits - (index + 1))) & 1
    if binary == 1:
      GPIO.output(SPI_MOSI, True)
      print("1")
      time.sleep(1)
    elif binary == 0:
      GPIO.output(SPI_MOSI, False)
      print("0")      
      time.sleep(1)
  GPIO.setup(SPI_SCLK, GPIO.OUT, initial=GPIO.LOW)