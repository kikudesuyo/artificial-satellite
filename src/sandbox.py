day = 31*24*60*60
hour = 24*60*60
minute = 60*60
second = 60

total_second = day + hour + minute + second
print(total_second)
print(2**22)
# hex_second = format(total_second, "x")
# print(len(hex_second))
# binary_second = format(total_second, "b")
# print(len(binary_second))
# aurora_percentage = 100
# print(len(format(aurora_percentage, "b")))
# heu = 40
# print(len(format(heu, "b")))
# saturation = 255
# value = 255


binary_day = format(31, "b")
binary_hour = format(24, "b")
binary_minute = format(60, "b")
binary_second = format(60, "b")
print(len(binary_day))
print(len(binary_hour))
print(len(binary_minute))
print(len(binary_second))