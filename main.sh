#!/bin/bash
python /home/i-spes/artificial_satellite/src/uart_communication.py 
#割り込み処理も書き込む
#もし命令がなかった場合にこのファイルでエラーが出るはず、その場合どうするのかを考える。

order=$(</home/i-spes/artificial_satellite/src/order/order.txt) 
if [ ${order} = 0X01 ]; then 
  python /home/i-spes/artificial_satellite/src/analysis/main.py
elif [ ${order} = 0X02 ]; then 
  python /home/i-spes/artificial_satellite/src/shooting/take_photograph.py
  done
elif [ ${order} = 0X03 ]; then
  python /home/i-spes/artificial_satellite/communication/main.py

elif [ ${order} = 0X04 ]; then
  sudo shutdown now
fi
