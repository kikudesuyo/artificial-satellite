#constant of order
DATA_SIZE_INDEX = 2

FORMAT_DATA_SIZE_MIN    =   5
FORMAT_ADRS             =   0
FORMAT_CMD              =   1
FORMAT_DATA_SIZE        =   2
FORMAT_DATA_START       =   3

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

#割り込みピンの設定(BORAD)
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


#MCとのシーケンス番号の確認
INITIAL_SEQUENCE_FLAG = False
