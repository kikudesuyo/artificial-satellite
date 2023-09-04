#constant of analysis 
AURORA_THREHOLD = 0.034004
MIN_HSV_RANGE = [40, 60, 0]
MAX_HSV_RANGE = [80, 245, 255]
IMAGE_SIZE = 2116800

#衛星打ち上げ時刻
MIN_WEEK_RANGE   = 0
MAX_WEEK_RANGE   = 50
MIN_HOUR_RANGE   = 0
MAX_HOUR_RANGE   = 24
MIN_MINUTE_RANGE = 0
MAX_MINUTE_RANGE = 60
MIN_SECOND_RANGE = 0
MAX_SECOND_RANGE = 120

#時刻データの既定値
ERROR_VALUE = 60480000

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

#状況
SHOOTING_COMPLETION = 0
OTHERS_COMPLETION = 1
SHOOTING_INTERRUPTION = 0
ANALYSIS_INTERRUPTION = 2
SPLIT_INTERRUPTION = 3
DOWNLINK_INTERRUPTION = 4