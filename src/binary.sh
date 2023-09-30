#画像のバイナリー化
# xxd -p "/c/Users/kikuh/OneDrive - Kyushu University/directory/artificial_satellite/img/downlink_img/compressed_img.jpg" "/c/Users/kikuh/OneDrive - Kyushu University/directory/artificial_satellite/data/downlink_data_sh.txt"

# バイナリー化したテキストファイルを復元
xxd -r -p "/c/Users/kikuh/OneDrive - Kyushu University/directory/artificial_satellite/data/downlink_data_sh.txt" "/c/Users/kikuh/OneDrive - Kyushu University/directory/artificial_satellite/img/restore_sh.jpg"