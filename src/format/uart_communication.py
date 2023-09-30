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

def receive_command(format_array=20*[0]):
  """コマンド受信関数

  Arg:
    format_array (list), optional): 空の配列を用意. Defaults to 20*[0].

  Return:'
    format_array (list): 受信後の配列
  """
  uart = UartCommunication()
  index = 0
  while True:
    #format_array[index] = int(binascii.hexlify(uart.receive_one_byte()), 16)
    format_array[index] = uart.receive_one_byte()
    if int(format_array[DATA_SIZE_INDEX], 16) != 0:
      total_data_size = int(format_array[DATA_SIZE_INDEX], 16) + 5
    if index + 1 == total_data_size:
      break
    index += 1
  uart.close()
  return format_array

def send_command(command):
  uart = UartCommunication()
  uart.send_data(command)
  uart.close()