
def execute_loop():
  import time
  from analysis.main import main
  # start = time.perf_counter()
  # print("start")
  # from main import main
  # end = time.perf_counter()
  # print("end")
  # print("handle time is: " + str(end - start))

  from util import generate_path

  absolute_path = generate_path("/data/execution_time.txt")
  sum = 0
  file = open(absolute_path, "a")
  for i in range(10):
    start = time.perf_counter()
    print("start")
    main() 
    end = time.perf_counter()
    print("end")
    exe_time = end - start
    print(f'handle time is {exe_time}')
    sum += end - start
    file.write(f'{i+1}: {exe_time} \n')
  mean = sum/10
  file.write(f'mean: {mean} \n\n')
  print(mean)