#SENDER:RPI
#撮影要求コマンドは予約コマンドのため応答はしない。
ACK_RPI_GS_SPLIT           = 3
ACK_RPI_GS_DONWLINK        = 4

CMD_RPI_CW_RESET           = 2

CMD_RPI_EPS_POWER_CHECK    = 2
CMD_RPI_EPS_SHUTDOWN       = 3
ACK_RPI_EPS_SHUTDOWN       = 4

ACK_RPI_MC_CW_DATA         = 2
CMD_RPI_MC_DOWNLINK        = 3
ACK_RPI_MC_DOWNLINK_FINISH = 4
CMD_RPI_MC_DATE            = 5

#RECEIVER:RPI
CMD_GS_RPI_SHOOTING        = 2
CMD_GS_RPI_SPLIT           = 3
CMD_GS_RPI_DOWNLINK        = 4
CMD_GS_RPI_ANALYSIS        = 5
CMD_GS_RPI_TASK_INFO       = 6

ACK_CW_RPI_RESET           = 2

ACK_EPS_RPI_POWER_CHECK    = 2
ACK_EPS_RPI_SHUTDOWN       = 3
CMD_EPS_RPI_SHUTDOWN       = 4

CMD_MC_RPI_CW_DATA         = 2
ACK_MC_RPI_DOWNLINK        = 3
CMD_MC_RPI_DOWNLINK_FINISH = 4
ACK_MC_RPI_DATE            = 5