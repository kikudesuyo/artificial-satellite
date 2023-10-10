# from analysis.main import main
# main()

# from flow.split import split_flow
# split_flow()


from downlink.uplink_edition import write_uplink_data_to_status
from downlink.status_edition import read_designed_packet, change_status_file


format_array = [34, 234, 7, 3, 23, 24, 64, 43, 53, 56, 34, 41]
format_array = [34, 234, 7, 3, 32, 5, 53, 14, 53, 23, 23, 24]
print(read_designed_packet())
change_status_file(1)
print(read_designed_packet())