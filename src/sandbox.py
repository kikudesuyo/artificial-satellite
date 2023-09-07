import pickle
from util import generate_path

def get_uplink_data():
  status_file = open(generate_path("/src/flow/downlink_status.txt"), "rb")
  designed_files = pickle.load(status_file)
  status_file.close()
  return designed_files
 
def output_downlink_status():
  status = get_uplink_data()
  if len(status) == 0:
    print("送ったオーロラデータだけを削除")
    #delete_files("送ったオーロラデータだけを削除")
  elif len(status) == 1:
    status[0] = status[0] + 1
  else:
    if status[1] == 0:
      print("ダウンリンク終了")
      pass
    else:
      del status[0]
  status_file = open(generate_path("/src/flow/downlink_status.txt"), "wb")
  pickle.dump(status, status_file)
  status_file.close()



#value = get_uplink_data()
#print(value)


output_downlink_status()

value_2 = get_uplink_data()
print(value_2)


