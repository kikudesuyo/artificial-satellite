# from format.uart_communication import send_command, receive_command

# format_array = 55 * ['0']
# raw_data = receive_command(format_array)
# print(raw_data)
# #もしraw_dataがbyte型なら以下のコードを使用してください
# int_format = list(map(ord, raw_data))
# hex_format = list(map(hex, int_format))
# print(int_format)
# print(hex_format)
  
# """撮影するなら以下のコードを使用してください"""
# # from shooting.take_photograph import take_photo
# # take_photo(shooting_times=5, shooting_interval_msec=1000)

from flow.split import split_flow

split_flow()