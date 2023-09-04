#constant of analysis 
AURORA_THREHOLD = 0.034004
MIN_HSV_RANGE = [40, 60, 0]
MAX_HSV_RANGE = [80, 245, 255]
IMAGE_SIZE = 2116800

#衛星打ち上げ時刻
MIN_WEEK_RANGE = 0
MAX_WEEK_RANGE = 50
#他の時刻データについても範囲を記述する
ERROR_VALUE = "" #この値は未定　１６進数の秒数データにする

#constant of SPI communication
MOSI = 19
MISO = 21
SCLK = 23

#constant of order
DATA_SIZE_INDEX = 2

#address 
GS_ADDR     =   0 
COM_ADDR    =   1
CW_ADDR     =   2
MAIN_ADDR   =   3
EPS_ADDR    =   4
ADCS_ADDR   =   5
MC_ADDR     =   6
CAM_ADDR    =   7
MAG_ADDR    =   8
INIT_ADDR   =   9

#割り込みピンの設定(BCM)
INTERRUPT_PIN = 12

#誤り判定
BUFFER_SIZE_COM    =  80
BUFFER_SIZE_EPS    =  80
BUFFER_SIZE_MC     =  80

DATA_CORRECT    =   1
DATA_OVERFLOW   =   0
DATA_CRC_ERROR  =   2
DATA_ADRS_ERROR =   3
DATA_TIMEOUT    =   4

#時刻の初期値
INITIAL_TIME_DATA = "0001/01/01 00:00:00"