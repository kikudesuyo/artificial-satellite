import time
from util import shutdown
import RPi.GPIO as GPIO
from constant.eps_relation import TX_EPS_RX_RPI, TX_RPI_RX_EPS

def callback_eps_shutdown():
  print("receive_shutdown_sign from io line")
  #shutdown()

def set_eps_callback():
  """起動後"""
  GPIO.add_event_detect(TX_EPS_RX_RPI, GPIO.RISING, callback = callback_eps_shutdown, bouncetime = 60000)


def input_from_eps():
  return GPIO.input(TX_EPS_RX_RPI)

def ack_shooting_request():
  GPIO.output(TX_RPI_RX_EPS, GPIO.HIGH)

def request_shutdown_flow():
  """ラズパイからのシャッtダウン要求"""
  GPIO.output(TX_RPI_RX_EPS, GPIO.HIGH)
  shutdown_count = 0
  while True:
    if input_from_eps():
      print("TX_EPS_HIGH")
      shutdown_count += 1
      time.sleep(0.5)
    else:
      print("TX_EPS_LOW")
      shutdown_count = 0
      time.sleep(1)
    if shutdown_count == 5:
      print("shutdown approved")
      shutdown()