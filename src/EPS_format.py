import time
from util import shutdown
import RPi.GPIO as GPIO
from constant import INTERRUPT_PIN_EPS_1, INTERRUPT_PIN_EPS_2 #INTERRUPT_PIN_EPSをEPSの人に聞く

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INTERRUPT_PIN_EPS_1, GPIO.IN, initial=GPIO.LOW)
GPIO.setup(INTERRUPT_PIN_EPS_2, GPIO.IN, initial=GPIO.LOW)#initialを決める


def read_EPS_interruption():
    while True:
        if GPIO.input(INTERRUPT_PIN_EPS_1): #GPIO.inputがHIGHのときはTrueを返す
            if GPIO.input(INTERRUPT_PIN_EPS_2):
                print("shutdown")
                #shutdown()
            else:
                print("")
        else:
            if GPIO.input(INTERRUPT_PIN_EPS_2):
                print("")
            else:
                pass
        time.sleep(1)#時間決める