from ast import Try
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures.thread import ThreadPoolExecutor

class ScrapingWebJob:
  profile = ''
  html = ""
  listJobs = []
  driver = webdriver.Chrome('C:\chromedriver.exe')
  
  def __init__(self):  
    self.driver.get("https://id.indeed.com/")
    time.sleep(3)
    
  def typingWhat(self):
    this = self
    elemInput = this.driver.find_element(By.ID, "text-input-what")
    elemInput.send_keys("marketing")
  
  def typingWhere(self):
    this = self
    elemInput = this.driver.find_element(By.ID, "text-input-where")
    elemInput.send_keys("jakarta")
  
  def clickFindJob(self):
    this = self
    btn = this.driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    btn.click()
    
  def recordWeb(self):
    this = self
    this.html = this.driver.find_element(By.XPATH, '//*[@id="resultsCol"]')
    with open("index.html", "w") as file:
      file.write(this.html.get_attribute('innerHTML'))      
    
    soup = BeautifulSoup(this.html.get_attribute('innerHTML'), "html.parser")
    
    try:
      for data in soup.select(".resultContent"):
        title = data.select(".jobTitle")[0]
        compName = data.select(".companyName")[0]
        
        jobs = {
          "title": title.text,
          "compName": compName.text,
        }
        
        this.listJobs.append(jobs)        
    except:
      print("error looping")    
    
    dumpListJobs = json.dumps(this.listJobs)
    writeJobs = open("jobs.json", "w")
    writeJobs.write(dumpListJobs)
    
    readJobs = open("jobs.json", 'r')
    loadReadJobs = json.load(readJobs)
    
    print(len(loadReadJobs))
    
    
    
  
scrapingWebJob = ScrapingWebJob()
scrapingWebJob.typingWhat()
scrapingWebJob.typingWhere()
scrapingWebJob.clickFindJob()
time.sleep(3)
scrapingWebJob.recordWeb()