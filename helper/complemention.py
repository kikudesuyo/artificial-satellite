def complement_datetime(datetime):
  "送信データはYYYYMMDDhhmmssと仮定"
  "データが正しい型ではなかったら規定値を出力"
  try:
    datetime = datetime.zfill(14)
    year = int(datetime[:4])
    if not (2100 > year > 2000):
      raise Exception
    month = int(datetime[4:6])
    if not (12 >= month >= 1):
      raise Exception
    day = int(datetime[6:8])
    if not (31 >= day >= 1):
      raise Exception
    hour = int(datetime[8:10])
    if not (23 >= hour >= 0):
      raise Exception
    minute = int(datetime[10:12])
    if not (59 >= minute >= 0):
      raise Exception
    second = int(datetime[12:14])
    if not (59 >= second >= 0):
      raise Exception
    datetime = f'{year}{month}{day}{hour}{minute}{second}'
  except:
    datetime = "20000101000000"
  return datetime

print(complement_datetime("20211021034523"))
