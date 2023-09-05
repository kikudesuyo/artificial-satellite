from helper.conditional_operation import does_front_handle

if does_front_handle():
  print("通信開始")
else:
  print("待機")