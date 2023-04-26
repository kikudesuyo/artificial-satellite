from util import generate_path

def get_packet(data_path):
  absolute_img_path = generate_path(data_path)
  data = open(absolute_img_path, "r", encoding="utf-8").read()
  split_str = [data[i:i+128] for i in range(0, len(data), 128)]
  count = 1
  for i in split_str:
    packet = generate_path("/data/packet/packet") + str(count) + ".txt"
    open(packet, "w").write(i)
    count += 1