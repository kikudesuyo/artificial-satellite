from communication.spi_slave import SpiCommunication

def main(sending_data, restart_index=0):
  """

  Arg:
    sending_data (list[str]):
    restart_index (int): 送信再開する配列のindex
  """
  spi = SpiCommunication()
  for packet_data in sending_data[restart_index:]:
    spi.send_data(packet_data)