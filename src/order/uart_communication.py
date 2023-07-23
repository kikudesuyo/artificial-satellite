import serial
import binascii
from constant import DATA_SIZE_INDEX

class UartCommunication():
  
  def __init__(self):
    self.ser = serial.Serial('/dev/ttyAMA0', 9600)

  def send_data(self, command):
    self.ser.write(command.encode("utf-8"))
    
  def receive_one_byte(self):
    command = self.ser.read()
    return command
  
  def close(self):
    self.ser.close()

def receive_command(format_array):
  uart = UartCommunication()
  index = 0
  while True:
    #format_array[index] = int(binascii.hexlify(uart.receive_one_byte()), 16)
    format_array[index] = uart.receive_one_byte()
    if index + 1 == format_array[DATA_SIZE_INDEX] + 5:
      break
    index += 1
  uart.close()
  return format_array

def send_command(command):
  uart = UartCommunication()
  uart.send_command(command)
  uart.close()