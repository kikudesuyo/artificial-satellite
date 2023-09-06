import serial
import time
import RPi.GPIO as GPIO
from constant import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INTERRUPT_PIN, GPIO.OUT, initial=GPIO.LOW)

def print_0xdata(data):
	data_x=[]
	for i in range(len(data)):
		data_x.append(format(data[i],'02x'))
	print(*data_x)
	print("")
        

adrs_list=[
    "GS",    
    "COM",   
    "CW",    
    "MAIN",  
    "EPS",   
    "ADCS",  
    "MC",    
    "CAM",   
    "MAG",   
    "init",
    ]

data_error=[
    "DATA_OVERFLOW",
    "DATA_CORRECT" ,
    "DATA_CRC_ERROR",
    "who is sender?",
    "DATA_TIMEOUT"
]

FORMAT_DATA_SIZE_MIN    =   5
FORMAT_ADRS             =   0
FORMAT_CMD              =   1
FORMAT_DATA_SIZE        =   2
FORMAT_DATA_START       =   3

get_COM_data=[0x00]*BUFFER_SIZE_COM
get_COM_data[FORMAT_ADRS]=INIT_ADDR
get_MC_data=[0x00]*BUFFER_SIZE_MC
get_MC_data[FORMAT_ADRS]=INIT_ADDR
get_EPS_data=[0x00]*BUFFER_SIZE_EPS
get_EPS_data[FORMAT_ADRS]=INIT_ADDR

def FORMAT_CRC_STRAT(array):
    return 3 + array[FORMAT_DATA_SIZE]
def FORMAT_FULL_SIZE(array):
    return FORMAT_DATA_SIZE_MIN + array[FORMAT_DATA_SIZE]
def FORMAT_ADRS_SENDER(array):
    return (array[FORMAT_ADRS] >> 4)
def FORMAT_ADRS_TARGET(array):
    return (array[FORMAT_ADRS] & 0x0f)

def get_data_from_format(format_array):
    """

    Arg:
      format_array (list[int]): 通信で形成する型
    Return:
      data (list[int]): データのみを抽出
    """
    data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
    return data

UART_TIMEOUT=   80
BUFFER_SIZE=    80
MY_ADDRESS = CAM_ADDR

GET_MC_DATA = [0]*BUFFER_SIZE
GET_MC_DATA[0] = INIT_ADDR

MC_line = serial.Serial('/dev/ttyAMA0',9600,timeout=1)

def from_micon():
    i=0
    receive_data=get_MC_data
    while True:
        #MC_line = serial.Serial('/dev/ttyAMA0',9600,timeout=1)
        
        data=MC_line.read(1)
        if len(data)==0:
            #print("none")
            return 0
        receive_data[i] = int(ord(data))
        if i == FORMAT_DATA_SIZE:
             if receive_data[i] > BUFFER_SIZE_MC:
                #print("over_flow")
                MC_line.read_all()
                return 0
        
        elif i>=FORMAT_DATA_SIZE and i+1 >= FORMAT_FULL_SIZE(receive_data):
             #print("success")
             break
        i+=1
        
    #print(receive_data)
    #MC_line.close()
    #print(FORMAT_ADRS_SENDER(receive_data))
    print("from_",end="")
    print(adrs_list[FORMAT_ADRS_SENDER(receive_data)],end="")
    print("_GET_DATA: ", end="")
    cut_data = receive_data[:FORMAT_FULL_SIZE(receive_data)]
    print_0xdata(cut_data)
    return_val = check_get_data(receive_data, BUFFER_SIZE_MC)
    if return_val == 1:
        print("data_collect")
    else:
        print(data_error[return_val])
        return 0
    return cut_data

def send_micon(SEND_DATA):
     #MC_line = serial.Serial('/dev/ttyAMA0',9600,timeout=None)
     MC_line.write(SEND_DATA)
     #MC_line.close()

def send_MC(send_data,transfer_frag = False):
    if(transfer_frag==False):
        add_my_address(send_data)
        #print_0xdata(send_data)
        add_CRC16(send_data,FORMAT_CRC_STRAT(send_data))
        #print_0xdata(send_data)
    format_data_print('send_MC:',send_data)
    GPIO.output(INTERRUPT_PIN,GPIO.HIGH)
    #time.sleep(0.02)
    send_micon(send_data)
    GPIO.output(INTERRUPT_PIN,GPIO.LOW)

def send_data(adrs, cmd, downlink_data,transfer_frag = False):
    send_mc_data=[0x00, 0x00, 0x00, 0x00, 0x00]
    if(transfer_frag==False):
        send_mc_data[FORMAT_ADRS] = adrs
        add_my_address(send_mc_data)
        send_mc_data[FORMAT_CMD] = cmd
        send_mc_data[FORMAT_DATA_SIZE] = len(downlink_data)
        send_mc_data[FORMAT_DATA_START:FORMAT_DATA_START] = downlink_data
        #print_0xdata(downlink_data)
        add_CRC16(send_mc_data,FORMAT_CRC_STRAT(send_mc_data))
        #print_0xdata(downlink_data)
    format_data_print(adrs_list[adrs],send_mc_data)
    GPIO.output(INTERRUPT_PIN,GPIO.HIGH)
    #time.sleep(0.02)
    send_micon(send_mc_data)
    GPIO.output(INTERRUPT_PIN,GPIO.LOW)

def send_CMD(adrs, cmd, transfer_frag = False):
    send_cmd_data=[0x00, 0x00, 0x00, 0x00, 0x00]
    if(transfer_frag==False):
        send_cmd_data[FORMAT_ADRS] = adrs
        add_my_address(send_cmd_data)
        send_cmd_data[FORMAT_CMD] = cmd
        #print_0xdata(send_data)
        add_CRC16(send_cmd_data,FORMAT_CRC_STRAT(send_cmd_data))
        #print_0xdata(send_data)
    format_data_print(adrs_list[adrs],send_cmd_data)
    GPIO.output(INTERRUPT_PIN,GPIO.HIGH)
    #time.sleep(0.02)
    send_micon(send_cmd_data)
    GPIO.output(INTERRUPT_PIN,GPIO.LOW)

def add_my_address(send_data):
	send_data[FORMAT_ADRS] |= MY_ADDRESS << 4

def check_get_data(get_data, buffer_size):
    if(FORMAT_FULL_SIZE(get_data)) > buffer_size:
        #print("buffer overflow\r\n")
        return DATA_OVERFLOW
    elif (check_CRC16(get_data, FORMAT_CRC_STRAT(get_data)) == False) :
        #print("CRC error\r\n")
        return DATA_CRC_ERROR
    elif (FORMAT_ADRS_TARGET(get_data) >= INIT_ADDR):
        #print("address error\r\n")
        return DATA_ADRS_ERROR
	
    else:
        return DATA_CORRECT
    
def check_interrupt(get_data):
	return FORMAT_ADRS_TARGET(get_data) != INIT_ADDR

def interrupt_end(get_data):
	get_data[FORMAT_ADRS] = INIT_ADDR
        
def calc_CRC16(data, size):
    crc = 0x0000	# 初期値（使用するのは下位16bitのみ）
    poly = 0x1021	# 生成多項式（X^16 + X^12 + X^5 + 1)。図1の緑ハッチ部分16bit
    
    for i in range(0, size):
        crc = crc ^ (data[i] << 8)  # CRCの上位8bitと入力データのXOR算
        
        for j in range(0, 8):
            
            if(crc & 0x8000 == 0x8000):
            	# crcの先頭ビットが1のとき、crcを「左に1bit」シフトし、生成多項式とXOR算
                crc = poly ^ ( crc << 1)
            else:
            	# crcの先頭ビットが0のとき、crcを「左に1bit」シフトするのみ
                crc = (crc << 1)
                
    return crc & 0xffff	#下位16bitのみが有効な計算値なので、0xffffでANDを取る

def add_CRC16( data, CRC_start_byte): 
	int16_to_8(data, calc_CRC16(data, CRC_start_byte))

def check_CRC16(data, CRC_start_byte):
	return int8_to_16(data[CRC_start_byte:]) == calc_CRC16(data, CRC_start_byte)


def format_data_print(data_name, data, buffer_size = 0xff):
    print('send_',end="")
    print(data_name, end='')
    print(":",end="")
    if FORMAT_FULL_SIZE(data) > buffer_size:
        print("print data overflow\r\n")
    else:
        print_0xdata(data)
    print("\r\n")

def int16_to_8(data,CRC16):
    CRC8_box=[0,0]
    for i in range(2):
        CRC8_box[i] = data[FORMAT_CRC_STRAT(data)]
    CRC8_box[0] = CRC16 >> 8
    CRC8_box[1] = CRC16 & 0xff
    CRC_byte=FORMAT_CRC_STRAT(data)
    data[CRC_byte]=CRC8_box[0]
    data[CRC_byte+1]=CRC8_box[1]
    return CRC8_box

def int8_to_16 (data):
	return (data[0] << 8) | (data[1] & 0xff)