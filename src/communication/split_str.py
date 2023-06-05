import serial
import binascii
import time
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout = 0.5)  #UART初期化

#コマンド送信
ser.write(b'1111')
#ser.write(b'\x22\x00\x00\x22') #4バイトのByte型でデータを送信
#ser.write(0x01)

#コマンドの結果を受信(4byte)
while True:
    data = ser.read(4)
    print(data)
    time.sleep(1)

#コマンドの結果を受信 #区切り文字0x0Aまでのデータを受信 read only 1 line.

#binデータで読み出されるので結果をhexに変換
#data=binascii.b2a_hex(data)
#print(data)
ser.close() # ポートのクローズ
print("finished")
