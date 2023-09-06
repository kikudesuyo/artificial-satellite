from util import shutdown
from flow.analysis import analysis_flow
from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow
from format.format import *
from helper.status_operation import handle_based_on_previous_status, is_equal_command, does_front_handle, main_check_communication_status, background_check_communication_status
from helper.file_operation import output_communication_status
from format.YOTSUBA_CMD_RPI import *
from constant import *
import time

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
        if CMD == ACK_MC_RPI_DOWNLINK_REQUEST_START: #ダウンリンク要請の返答コマンド
            print("down_prepare")
            downlink_flow()

        elif CMD == ACK_MC_RPI_DOWNLINK_REQUEST_POSTPONE: #通信継続要請の返答
            #SPI継続
            print("downlink_postpone")
        
        else :
            print("NO_CMD")
    elif SENDER == MC_ADDR:
        if CMD == CMD_MC_RPI_


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
    #send_CMD(MC_ADDR,CMD_RPI_MC_POWER_ON)#起動完了
    handle_based_on_previous_status()
    try:
        last_format_array = None
        while True:
            i = 0
            while True:
                if main_check_communication_status():#statusファイルの居場所を変更してもいいかも
                    print("break!!")#ここの挙動をraspiで確認した方がいい。一つ上のwhile trueのループがどうまわるか
                    time.sleep(10)
                    break
                elif i < 5:#この回数も決めた方がいい。どの程度待ってエラーが起きていると判断するか
                    print("sleep!")
                    time.sleep(5) #ここの時間は要相談, また、この時命令を送り続けてもらうようにする必要あり
                    i += 1
                else:
                    print("Error! Background communication does not end or communication_status is not correct!")
                    output_communication_status(NONE_COMMUNICATING)#ここの例外処理の相談した方がいい、例外処理の方法そのものや、例外処理の回数などを相談する。bacgroundも注意
                    return
            output_communication_status(MAIN_COMMUNICATING)
            cmd_list = run()
            output_communication_status(NONE_COMMUNICATING)
            for format_array in cmd_list:
                if last_format_array == None:
                    selection(format_array)
                    last_format_array = format_array
                else:
                    if is_equal_command(format_array, last_format_array):
                        print("same command")
                        continue
                    else: 
                        selection(format_array)
                        last_format_array = format_array
    except Exception as e:
        print(e)
        pass

def background():
    try:
        while True:
            i=0
            while True:
                if background_check_communication_status():
                    time.sleep(5)
                    print("break")
                    break
                elif i < 5:
                    print("sleep!")
                    time.sleep(5) #ここの時間は要相談, また、この時命令を送り続けてもらうようにする必要あり
                    i += 1
                else:
                    print("This is the error! Background communication does not end or communication_status is not correct!")
                    output_communication_status(NONE_COMMUNICATING)#ここの例外処理を相談した方がいい。例外処理の方法そのものや、例外処理の回数を相談する。mainも注意
                    return
            output_communication_status(BACKGROUND_COMMUNICATING)
            cmd_list=run() #runを書き換えてもいいかも。引数↑で↓は最後に加える
            output_communication_status(NONE_COMMUNICATING)
            if does_front_handle():
                for format_array in cmd_list:
                    try:
                        interruption(format_array)
                    except Exception as e:
                        print(e)
                        pass
            else:
                time.sleep(5)
    except Exception as e:
        print(e)
        pass
