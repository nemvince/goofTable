from selenium import webdriver
import time
import json

class SeleniumScraper:
  def __init__(self, logger):
    self.logger = logger
    # Create a new instance of the Chrome driver
    try:
      self.driver = webdriver.Chrome()
    except Exception as e:
      self.logger.error(f"Failed to create a new instance of the Chrome driver: {e}")
      exit()

  def scrapeRequestsToFile(self, url = "https://petrik.edupage.org/timetable/"):
    # Navigate to the URL
    self.driver.get(url)
    
    time.sleep(2)

    logs = self.driver.get_log('performance')
    network_logs = [json.loads(log['message'])['message'] for log in logs if json.loads(log['message'])['message']['method'] == 'Network.requestWillBeSent']
    target_requests = []
    for log in network_logs:
      if "__func" in log['params']['request']['url']:
        target_requests.append(log)

    self.driver.quit()
    if not target_requests:
      self.logger.error("No target requests found")
      exit()
    idx = 0

    for request in target_requests:
      if idx == 0:
        filename = "ttv"
      else:
        filename = "reg"
      idx += 1
      with open(f"req/{filename}.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(request, indent=4))
