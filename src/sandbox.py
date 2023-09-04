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

list = [1, 143, 5, 42, 22, 53, 93, 63, 13, 53, 53, 12, 93]
print(list[3:list[2]+3])

print(int(0.5))