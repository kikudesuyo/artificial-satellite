import RPi.GPIO as GPIO

from constant.format import INTERRUPT_PIN
from constant.eps_relation import TX_EPS_RX_RPI, TX_RPI_RX_EPS

def set_gpio_line():
  GPIO.setwarnings(False)
  GPIO.cleanup()
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(INTERRUPT_PIN, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(TX_EPS_RX_RPI, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(TX_RPI_RX_EPS, GPIO.OUT, initial=GPIO.LOW)