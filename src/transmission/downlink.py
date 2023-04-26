# !/usr/bin/env python
import RPi.GPIO as GPIO
import time
import re
Vref = 2.048
SPI_CLK = 23
SPI_MISO = 21

#print(GPIO.input(SPI_CLK))
#print(type(GPIO.input(SPI_CLK)))

def init():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # GPIO
        GPIO.setup(SPI_MISO, GPIO.OUT)
        GPIO.setup(SPI_CLK, GPIO.IN)
        GPIO.output(SPI_MISO, GPIO.LOW)
        print("Done")


def spi_1byte_write(data):
    count =0
    for i in range(8):
        while GPIO.input(SPI_CLK) == False:
            {}
        if (data >> (7 - i)) & 1:
            #print('1')    
            GPIO.output(SPI_MISO, GPIO.HIGH)
        else:
            #print('0')
            GPIO.output(SPI_MISO, GPIO.LOW)
        #time.sleep(1)
        print(count)
        count += 1
        while GPIO.input(SPI_CLK) == True:
            {}
    
    
    
    
    
"""
def atoi(char):
    if (char == '0'):
       num = 0x00
    elif (char == '1'):
        num = 0x01
    elif (char == '2'):
        num = 0x02
    elif (char == '3'):
        num = 0x03
    elif (char == '4'):
        num = 0x04
    elif (char == '5'):
        num = 0x05
    elif (char == '6'):
        num = 0x06
    elif (char == '7'):
        num = 0x07
    elif (char == '8'):
        num = 0x08
    elif (char == '9'):
        num = 0x09
    elif (char == 'a'):
        num = 0x0A
    elif (char == 'b'):
        num = 0x0B
    elif (char == 'c'):
        num = 0x0C
    elif (char == 'd'):
        num = 0x0D
    elif (char == 'e'):
        num = 0x0E
    elif (char == 'f'):
        num = 0x0F
    
    return num


def str_int_list(str_list):
    atoi_list = []
    for i in range(len(str_list)):
        if (i % 2):
            atoi_list.append(atoi(str_list[i]))
        else:
            #atoi_list[i - 1] <<= 4
            #atoi_list[i - 1] |= atoi(str_list[i])
                   
    return atoi_list              
                   
   
hex_list = ["ab", "1b", "4c", "7d", "2e", "1f"]
file = open("/home/i-spes/satellite_main/sora/num1.txt", "r")
string = file.read()
# int_string = int(string, 16)
split_string = re.split("(..)", string)[1::2]

str_int_list(string) 
#print(split_string)
#split_string = list(map(str ,split_string))
#print(type(split_string))
#print(split_string)
#split_string = split_string.replace("'", "")
#
#print(split_string)
split_list =[]
for i in range(len(split_string)):
               int_split_string = int(split_string[i], 16)
               hex_split_string = hex(int_split_string)
               split_list.append(hex_split_string)
#print(split_list)
#int_split_string = int(split_list,16)
#for i in range(len(split_string):
#   if split_string[i] in hex_list = True:
               
#print(int_split_string)
#print(type(int_split_string))
# split_int =list(map(int, split_string))
print(type(split_list[1]))
"""

data = [0x3a, 0x4e, 0xf2, 0xee]

def downlink():
    for i in range(len(data)):
        #int_data = int(split_list[i], 16)
        #hex_data = hex(int_data)
        #print(type(hex_data))
        spi_1byte_write(data[i])
    print("finish")













































































































































































































init()
downlink()

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