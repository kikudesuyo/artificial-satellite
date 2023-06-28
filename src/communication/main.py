from communication.spi_slave import init, send_data

def main(sending_data):
  """

  Arg:
      sending_data (list): str配列
  """
  init()
  for packet_data in sending_data:
    send_data(packet_data)

main()