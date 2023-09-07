import pickle
from util import generate_path

list = ["hoge",2,3,4]
downlink_write = open(generate_path("/src/flow/downlink_status.txt"), "wb")
pickle.dump(list, downlink_write)
downlink_write.close()

downlink_read = open(generate_path("/src/flow/downlink_status.txt"), "rb")
downlink_files = pickle.load(downlink_read)
downlink_read.close()
print(downlink_files)
print(type(downlink_files[0]))