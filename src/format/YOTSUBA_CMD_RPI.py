#先が送信、後が受信
#CMDが能動的、ACKが受信してから送信
#CMD_EPS_RPI
CMD_EPS_RPI_SHUTDOWN_REQUEST    =   0
ACK_EPS_RPI_ANALISYS            =   1



#CMD_RPI_EPS
CMD_RPI_EPS_ANALISYS__REQUEST   =   0
CMD_RPI_EPS_SPLIT_DATA_REQUEST  =   1
ACK_RPI_EPS_SHUTDOWN            =   2


#CMD_GS_RPI
CMD_GS_RPI_DATA_REQUEST = 1
CMD_GS_RPI_SHOOTING     = 2
CMD_GS_RPI_SPLIT_DATA  =   3

#CMD_RPI_COM
CMD_RPI_COM_DOWNLINK_REQUEST    = 1
CMD_RPI_COM_DOWNLINK_FINISH     = 0
ACK_RPI_COM_DOWNLINK_TIMEOUT    = 2


#CMD_COM_RPI
ACK_COM_RPI_DOWNLINK_REQUEST_START      = 1
ACK_COM_RPI_DOWNLINK_REQUEST_POSTPONE   = 0
ACK_COM_RPI_DOWNLINK_FINISH             = 2
CMD_COM_RPI_DOWNLINK_TIMEOUT            = 3


#CMD_RPI_MC
    #DOWN_LINK
CMD_RPI_MC_DOWNLINK_REQUEST = 1
CMD_RPI_MC_DOWNLINK_FINISH  = 0
ACK_RPI_MC_SHOOTING_START   = 2 #ACK_TAIMESTAMP
ACK_RPI_MC_SHOOTING_FINISH  = 3
ACK_RPI_MC_ANALISYS_START   = 4
CMD_RPI_MC_ANALISYS_FINISH  = 5
ACK_RPI_MC_SPLIT_DATA_START = 6
CMD_RPI_MC_SPLIT_DATA_FINISH= 7
CMD_RPI_MC_POWER_ON         = 8




#CMD_MC_RPI
ACK_MC_RPI_DOWNLINK_REQUEST     = 1
ACK_MC_RPI_DOWNLINK_FINISH      = 0
CMD_MC_RPI_TIME_STUMP           = 2
CMD_MC_RPI_SHOOTING_REQUEST     = 3
CMD_MC_RPI_ANALISYS_REQUEST     = 4
CMD_MC_RPI_SPLIT_DATA_REQUEST   = 5
