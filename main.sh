#!/bin/bash

python /home/i-spes/satellite_main/implementation/order.py 
#OBCからの命令をテキストファイルに出力するpythonファイル
#九工大のファイルで通信関係のコードは全部pythonで書かれていたので、pythonファイルにしてます
#このファイルは全体を無限ループでまわす予定
#もし命令がなかった場合にこのファイルでエラーが出るはず、その場合どうするのかを考える。
#特にorder.txtが生成されないと一つ下のコードでエラーが出るので、それを避ける処理が必要

order=$(</home/i-spes/satellite_main/implementation/order/order.txt) 
#OBCからの命令が書かれた"xxx.txt"ファイルを読み込む。"order"という変数に命令を入れている。
#order.txtのpathをちゃんと書き直すこと
if [ ${order} = 0X01 ]; then 
#例えば"order"が"aaa"だったとき、pythonで aaa.pyというファイルを実行する
  echo success
  #order.txtを削除して次にOBCから命令が来た時に備える。
elif [ ${order} = 0X02 ]; then 
#例えば"order"が"bbb"だったとき, カメラで撮影する
  python /home/i-spes/artificial_satellite/src/shooting/take_photograph.py
    #tempファイルにすべき
  done

elif [ ${order} = 0X03 ]; then
  python main.py
  xxd -p /home/i-spes/satellite_main/implementation/image/aurora/downlink/downlink.jpg /home/i-spes/satellite_main/implementation/downlink/downlink_whole/downlink_whole.txt
  python split_txt.py
  python send_packet.py

elif [ ${order} = 0X04 ]; then
  sudo shutdown now
  #シャットダウン用のコマンド
fi

rm /home/i-spes/satellite_main/implementation/order/order.txt #場所を変更したので確認
echo success!