from GetSchedule import GetSchedule
import time
import threading
from concurrent.futures import ThreadPoolExecutor

def main():

  start = time.time()

  with open("systems.txt", "r") as file:
    lines = file.read().splitlines()
    url = lines[0] #first line always the url
    name = lines[1] # second line always the name
    max_thread = int(lines[2])
    systems = lines[3:]

  getSchedule = GetSchedule(url, name, max_thread)
  threads = []


  for system in systems:
    t = threading.Thread(target=getSchedule.get_schedule, args=(system,))
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  
  print("all done")
  end = time.time()
  print(f"execution time: {end - start}")

if __name__ == "__main__":
  main()