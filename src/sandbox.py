from flow.downlink import get_downlink_data
from downlink.downlink_status_edition import read_designed_packet, write_designed_nums

write_designed_nums([12, 34, 56])
print(read_designed_packet())
print(get_downlink_data())