from util import shutdown
from flow.analysis import analysis_flow
#from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow
from format.format import *
from helper.conditional_operation import handle_based_on_previous_status
from YOTSUBA_CMD_RPI import *
from constant import *

def run():
    cmd_list=[]
    while True:
        format_array = from_micon()
        if format_array==0:
            if len(cmd_list) != 0:
                print("receive_data:",end="")
                for l in cmd_list:
                    print_0xdata(l)
            break
        else:
            cmd_list.append(format_array)
    return cmd_list

def selection(format_array):
    SENDER = FORMAT_ADRS_SENDER(format_array)
    CMD    = format_array[FORMAT_CMD]
    
    if SENDER == EPS_ADDR:
        if CMD == CMD_EPS_RPI_SHUTDOWN_REQUEST:
            print("shut_down")
            send_CMD(EPS_ADDR, ACK_RPI_EPS_SHUTDOWN)
            #shutdown()
 
        elif CMD == ACK_EPS_RPI_ANALYSIS:
            #撮影後に継続したとき
            #send_CMD(EPS_ADDR,ACK_RPI_EPS_ANALYSIS_START)
            print("analysis_start")
            analysis_flow()
            print("analysis finish")
            send_CMD(EPS_ADDR, CMD_RPI_EPS_SHUTDOWN)
            print("shutdown")
            
        elif CMD == ACK_MC_RPI_DOWNLINK_REQUEST: #ダウンリンク指示コマンド
            print("down")
            #データ送信の準備プログラムを走らせる。
        else :
            print("NO_CMD")
    if SENDER == COM_ADDR:
        if CMD == ACK_COM_RPI_DOWNLINK_REQUEST_START: #ダウンリンク要請の返答コマンド
            print("down_prepare")
            downlink_flow()

        elif CMD == ACK_COM_RPI_DOWNLINK_REQUEST_POSTPONE: #通信継続要請の返答
            #SPI継続
            print("downlink_postpone")
        
        else :
            print("NO_CMD")
            
    elif SENDER == GS_ADDR:
        if CMD == CMD_GS_RPI_DATA_REQUEST: #ダウンリンク指示コマンド
            print("down")
            #データ送信の準備プログラムを走らせる。

        elif CMD == CMD_GS_RPI_SHOOTING:#時刻データ(撮影指示コマンド)
            print("shooting")
            send_CMD(MC_ADDR, ACK_RPI_MC_SHOOTING_START)
            time_data = format_array[FORMAT_DATA_START: FORMAT_DATA_START + format_array[FORMAT_DATA_SIZE]]
            print(time_data)
            shooting_flow(time_data)
            print("SHOOTING_FINISH")
            #継続可能かどうか尋ねる
            send_CMD(EPS_ADDR, CMD_RPI_EPS_ANALYSIS_REQUEST)
        
        elif CMD == CMD_GS_RPI_SPLIT_DATA:
            print("ACK_RPI_MC_SPLIT_DATA_START")
            send_CMD(MC_ADDR, ACK_RPI_MC_SPLIT_DATA_START)
            print("split")
            split_flow()
            print("CMD_RPI_MC_SPLIT_DATA_FINISH")
            time.sleep(1)
            send_CMD(MC_ADDR, CMD_RPI_MC_SPLIT_DATA_FINISH)
            #uplink_ack
        else :
            print("NO_CMD")

#バックグラウンドのシャットダウン用e
def interruption(format_array):
    SENDER = FORMAT_ADRS_SENDER(format_array)
    CMD    = format_array[FORMAT_CMD]
    
    if SENDER == EPS_ADDR:
        if CMD == CMD_EPS_RPI_SHUTDOWN_REQUEST:
            print("background_shut_down")
            send_CMD(EPS_ADDR, ACK_RPI_EPS_SHUTDOWN)
            #shutdown()
    
def main():
    send_CMD(MC_ADDR,CMD_RPI_MC_POWER_ON)#起動完了
    handle_based_on_previous_status()
    try:
        while True:
            cmd_list=run()
            last_format_array = []
            for index, format_array in enumerate(cmd_list):
                if index == 0:
                    selection(format_array)
                    last_format_array = format_array
                else:
                    if last_format_array != format_array:
                        selection(format_array)
                        last_format_array = format_array
                    else: 
                        print("same command")
                        continue
    except Exception as e:
        print(e)
        pass

def background():
    try:
        while True:
            cmd_list=run()
            for format_array in cmd_list:
                interruption(format_array)
    except Exception as e:
        print(e)
        pass