#!/bin/bash

python /home/i-spes/satellite_main/implementation/order.py #OBCからの命令をテキストファイルに出力するpythonファイル
#出力するテキストファイルは"xxx.txt"と仮定して、下で使っている
#九工大のファイルで通信関係のコードは全部pythonで書かれていたので、pythonファイルにしてます
#とりあえず、xxx.pyはpythonで"xxx.txt"に命令を書き込むだけのファイルでもいいと思う。
#このファイルは全体を無限ループでまわす予定
#もし命令がなかった場合にこのファイルでエラーが出るはず、その場合どうするのかを考える。
#特にorder.txtが生成されないと一つ下のコードでエラーが出るので、それを避ける処理が必要

order=$(</home/i-spes/satellite_main/implementation/order/order.txt) #OBCからの命令が書かれた"xxx.txt"ファイルを読み込む。"order"という変数に命令を入れている。
#order.txtのpathをちゃんと書き直すこと

#"order"がxxxのとき、特定のファイルを実行するというif文を書く
if [ ${order} = 0X01 ]; then #例えば"order"が"aaa"だったとき、pythonで aaa.pyというファイルを実行する
  echo success
  #order.txtを削除して次にOBCから命令が来た時に備える。
#ここまでは確認ずみ
elif [ ${order} = 0X02 ]; then #例えば"order"が"bbb"だったとき, カメラで撮影する
  for i in {1..3} ; do
    folder=/home/i-spes/satellite_main/implementation/image/temp/
    file=image${i}.jpg
    raspistill -w 1960 -h 1080 -o ${folder}${file} -t 10000 #tempファイルにすべき
    sleep 1 #1秒間待つ
  done
  python /home/i-spes/satellite_main/implementation/dark_distinguish.py
  rm /home/i-spes/satellite_main/implementation/image/temp/*.jpg
  rm /home/i-spes/satellite_main/implementation/image/nonaurora/*.jpg
  #python /home/i-spes/satellite_main/implementation/brightness.py

elif [ ${order} = 0X03 ]; then
  python resize.py
  xxd -p /home/i-spes/satellite_main/implementation/image/aurora/downlink/downlink.jpg /home/i-spes/satellite_main/implementation/downlink/downlink_whole/downlink_whole.txt #downlink.jpgをバイナリ化した文字列をccc.txtに出力
  python split_txt.py #ccc.txtに出力した文字列を区切る
  python send_packet.py

elif [ ${order} = 0X04 ]; then
  sudo shutdown now
  #シャットダウン用のコマンド
fi

rm /home/i-spes/satellite_main/implementation/order/order.txt #場所を変更したので確認
echo success!