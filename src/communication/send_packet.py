import serial
import binascii
import glob
import time

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=2)
path_list = glob.glob('/home/i-spes/satellite_main/implementation/downlink/packet/*.txt')
path_list.sort()
for i, path in enumerate(path_list):
    file = open(path, 'rb')  
    data = file.read()
    ser.write(data)
    #time.sleep(3)
    file.close()
ser.close()