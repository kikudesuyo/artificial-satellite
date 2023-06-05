# !/usr/bin/env python
import RPi.GPIO as GPIO
import time

SPI_CLK = 23
SPI_MISO = 21

def init():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # GPIO
        GPIO.setup(SPI_MISO, GPIO.OUT)
        GPIO.setup(SPI_CLK, GPIO.IN)
        GPIO.output(SPI_MISO, GPIO.LOW)
        print("Done")

"""
 void spi_1byte_write(int8 data) {
	for (int8 bit = 7; ; ) {
		if (input(SCK)) {
			if ((data >> bit) & 0x01) {
				output_high(MISO);
			}
			else {
				output_low(MISO);
			}
			bit--;
		}
		
		if (bit == 0) {
			break;
		}
		
		while (input(SCK) == 1) {
			;
		}
		while (input(SCK) == 0) {
			;
		}
	}
}
"""

# def startADC():
#         GPIO.output(SPI_CLK, GPIO.LOW) # Start with clock low
#         data = '00001000'
#         for i in list(data) :
#                 if i=='0' :
#                         clk_low() 
#                 else:
#                         clk_high() 
#         print ("Start ")
 
# def clk_high() :
#         GPIO.output(SPI_CLK, GPIO.HIGH) # Clock pulse
#         GPIO.output(SPI_MOSI,GPIO.HIGH) # Dout High
#         GPIO.output(SPI_CLK, GPIO.LOW)
#         GPIO.output(SPI_MOSI,GPIO.LOW)
 
# def clk_low() :
#         GPIO.output(SPI_CLK, GPIO.HIGH) # Clock pulse
#         GPIO.output(SPI_MOSI,GPIO.LOW)  # Dout Low
#         GPIO.output(SPI_CLK, GPIO.LOW)
 
# def resetADC():
#         GPIO.output(SPI_CLK, GPIO.LOW) # Start with clock low
#         GPIO.output(SPI_CS, GPIO.LOW)  # Enable chip
#         data = '00000110'
#         for i in list(data) :
#                 if i=='0' :
#                         clk_low() 
#                 else:
#                         clk_high() 
#         print ("reset ") 
#         GPIO.output(SPI_CS, GPIO.HIGH) # Disable chip
#   
# def sign16(x):
#         return ( -(x & 0b1000000000000000) |
#                   (x & 0b0111111111111111) )
 
# #main
# init()
# resetADC()
# try :
#         while 1:
#                 GPIO.output(SPI_CS, GPIO.LOW) # Enable chip
#                 startADC() 
#                 data = readADC()
#                 GPIO.output(SPI_CS, GPIO.HIGH) # Disable chip
#                 print round((Vref * (sign16(int(hex(data),16))) / 32767.0),5),"V "
#                 time.sleep(1)
# except :
#          GPIO.cleanup()
# GPIO.cleanup()