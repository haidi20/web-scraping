import time
import asyncio
import chromedriver_binary 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from concurrent.futures.thread import ThreadPoolExecutor

class ScrapingWebJob:
  profile = ''
  html = ""
  driver = webdriver.Chrome('C:\chromedriver.exe')
  
  def __init__(self):  
    self.driver.get("https://id.indeed.com/")
    time.sleep(3)
    
  def typingWhat(self):
    this = self
    elemInput = self.driver.find_element_by_id("text-input-what")
    elemInput.send_keys("marketing")
  
  def typingWhere(self):
    this = self
    elemInput = self.driver.find_element_by_id("text-input-where")
    elemInput.send_keys("jakarta")
  
  def clickFindJob(self):
    this = self
    btn = self.driver.find_element_by_class_name("yosegi-InlineWhatWhere-primaryButton")
    btn.click()
    
  def recordWeb(self):
    this = self
    this.html = self.driver.find_element_by_tag_name("span")
    with open("index.html", "w") as file:
      file.write(this.html.get_attribute('innerHTML'))
    
    
    
  
scrapingWebJob = ScrapingWebJob()
scrapingWebJob.typingWhat()
scrapingWebJob.typingWhere()
scrapingWebJob.clickFindJob()
time.sleep(3)
scrapingWebJob.recordWeb()