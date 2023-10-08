def split_string(string):
  """ダウンリンクするために文字列を配列に格納
  
  Arg:
    string (str):
  Return:
    format_data (list[int]): 1byteを1つの要素
      e.g.) format_data = [15, 3d, a1, 93]
  """
  print(string)
  format_data = [int(string[x:x+2], 16) for x in range(0, len(string), 2)]
  return format_data
