import serial
import time

from util import generate_path

class UartCommunication():
  
  def __init__(self):
    self.ser = serial.Serial('/dev/ttyAMA0', 9600)

  def send_data(self, command):
    self.ser.write(command.encode("utf-8"))
    
  def receive_data(self, string_length):
    command = self.ser.read(string_length)
    return command
  
  def close(self):
    self.ser.close()

uart = UartCommunication()
uart.send_command("1234")
command = uart.receive_command()
uart.close()

def receive_command(string_length):
  uart = UartCommunication()
  while True:
    command = uart.receive_command(string_length)
    if command != "":
      break
    time.sleep(0.1)

def send_command(command):
  uart = UartCommunication()
  uart.send_command(command)