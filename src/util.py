from pathlib import Path

def generate_path(path):
  """絶対パスを生成する

  Args:
    path (str): artificial_satellite/からの絶対パス

  Return:
      str: 引数pathへの絶対パス
  """
  return str(Path(__file__).parents[1]) + path  