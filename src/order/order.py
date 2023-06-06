#ここから
import comtest #これが何かわからない。多分UARTに使うやつ

from util import generate_path

uart=comtest.UART()
order = uart.receive_serial() #UART通信
#ここまで

#raspiが何をするかを指定するだけの命令の場合の処理
if len(order) == 4:
  f = open('/home/i-spes/satellite_main/integration/order/order/order.txt', 'w')
  f.write(order)
  f.close()

#raspiから写真を下ろすときの場合の処理。この時、(i)raspiが何をするかの指定の命令　(ii)下ろす写真の番号
#の2種類を指定する必要があるので、別処理
else:
  hex_order=order[0:4]
  num_order=order[4:]
  f = open(generate_path("/src/order/order.txt", ))
  f.write(hex_order)
  f.close()
  f = open(generate_path("/src/order/number.txt", "w"))
  f.write(num_order)
  f.close()