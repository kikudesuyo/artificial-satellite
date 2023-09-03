from util import shutdown, set_date_on_raspi, delete_files
from flow.analysis import analysis_flow
from flow.downlink import downlink_flow
from flow.shooting import shooting_flow
from flow.split import split_flow
from format.format import *
from YOTSUBA_CMD_RPI import *
from constant import *


now_task = 0
taskflag=0 #finished=0/unfinished=1
task_fin=["finished","unfinished"]

shooting = 1
analysis = 2
split    = 3

task_name=["FIRST_TIME",
      "shooting",
      "analysis",
      "split"
     ]

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
            #regist_now_task(now_task,taskflag)
            #shutdown()
 
        elif CMD == ACK_EPS_RPI_ANALISYS:
            send_CMD(MC_ADDR,ACK_RPI_MC_ANALISYS_START)
            print("analysis_start")
            analysis_flow()
            send_CMD(MC_ADDR, CMD_RPI_MC_ANALISYS_FINISH)
            
            #send_MC([0x74,0x02,0x00,0x00,0x00]) #解析終了コマンド
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
            print("photo")
            send_CMD(MC_ADDR, ACK_RPI_MC_SHOOTING_START)
            now_task = 1
            taskflag = 1
            #time_data = receive_command(15)
            #set_date_on_raspi(time_data)
            shooting_flow()
            taskflag = 0
            print("ACK_RPI_MC_SHOOTING_FINISH")
            send_CMD(MC_ADDR,ACK_RPI_MC_SHOOTING_FINISH)
            #send_MC([0x74,0x02,0x00,0x00,0x00]) #撮影終了コマンド(MC)
        
        elif CMD == CMD_GS_RPI_SPLIT_DATA:
            print("ACK_RPI_MC_SPLIT_DATA_START")
            send_CMD(MC_ADDR, ACK_RPI_MC_SPLIT_DATA_START)
            print("split")
            now_task = 2
            taskflag = 1 
            #delete_files("/data/aurora_img")
            #convert_img_into_text("/img/downlink_img/compressed_img.jpg")
            #split_text_string("/data/downlink_data.txt")
            split_flow()
            print("CMD_RPI_MC_SPLIT_DATA_FINISH")
            time.sleep(1)
            send_CMD(MC_ADDR, CMD_RPI_MC_SPLIT_DATA_FINISH)
            taskflag =0
            #uplink_ack
        else :
            print("NO_CMD")
            
def check_my_task():
    print("check_task")
    with open('task.txt', encoding="utf-8") as rf:
        task = int(rf.read())
        #print(task)
    if task == 0x00:
        #print("FIRST_TIME")
        return 0
    elif(task&0x01)==0:
        print("new_task")
        next_task = (task>>1)+1
        if next_task >= 3:
           next_task = 1
        
    else:
        print("task_continue")
        next_task = task>>1
    return next_task
    
def regist_now_task(task,flag):
    task = (task<<1) | flag
    print("regist_task:",end="")
    print(task_name[task])
    with open('task.txt','w') as wf:
        wf.write(str(task))
    
        

def main():
    MC_line = serial.Serial('/dev/ttyAMA0',9600,timeout=0)
    send_CMD(MC_ADDR,CMD_RPI_MC_POWER_ON)#起動完了
    #task = check_my_task()
    #print(task)
    #print(task_name[task])
    
    try:
        while True:
            cmd_list=run()
            for format_array in cmd_list:
                selection(format_array)
    except Exception as e:
        print(e)
        pass