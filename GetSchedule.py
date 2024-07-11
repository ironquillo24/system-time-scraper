from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import threading

class GetSchedule:
  def __init__(self, url, name, max_threads):
    self._lock = threading.Lock()
    self._url = url
    self._name = name
    self._semaphore = threading.Semaphore(max_threads)

  def get_schedule(self, system):
    with self._semaphore:
      print(f"running {system}")
      service = Service(executable_path="chromedriver.exe")
      options = Options()
      options.add_argument('--headless=new')
      driver = webdriver.Chrome(service=service, options=options)
      #driver = webdriver.Chrome(service=service)

      driver.maximize_window()
      driver.get(self._url)
      time.sleep(1)

      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-search"))) 

      driver.find_element(By.CLASS_NAME, "btn-search").click()
      input = driver.find_element(By.CSS_SELECTOR, "input.form-control")
      input.send_keys(system + Keys.ENTER)

      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-view")))
      driver.find_element(By.CLASS_NAME, "btn-view").click()
      driver.find_element(By.CLASS_NAME, "btn-close").click() 

      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "equipment-name-container"))) 
      driver.find_element(By.CLASS_NAME, "equipment-name-container").click()

      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "request-details-container")))

      schedules = driver.find_elements(By.CLASS_NAME, "request-details-container")

      with self._lock:
        for schedule in schedules:
          details = schedule.text.splitlines()
          if self._name in details:
            with open("myschedule.txt", "a") as f:
              f.write(system + " " + " ".join(details) + '\n')

      driver.quit()