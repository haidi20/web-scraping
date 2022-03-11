import re
import time
import json
from ast import Try
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.webdriver.support import expected_conditions as EC

class ScarpingPortalJob:
  html = ""
  profile = ''
  linkPortalJob = "https://id.indeed.com"
  listJobs = []
  driver = webdriver.Chrome('C:\chromedriver.exe')
  
  def __init__(self):  
    self.driver.get(self.linkPortalJob)
    time.sleep(3)
    
  # for bs4
  def getLinks(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
    return links
    
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
    try:
        this.html = WebDriverWait(this.driver, 30).until(
            EC.presence_of_element_located((By.ID, "pageContent"))
        )
    finally:
      # this.html = this.driver.find_element(By.TAG_NAME, 'table') 
      # with open("index.html", "w") as file:
      #   file.write(this.html.get_attribute('innerHTML'))      
      
      soup = BeautifulSoup(this.html.get_attribute('innerHTML'), "html.parser")
      
      try:
        if len(soup.select(".mosaic-zone")[1]) > 0:
          for data in soup.select(".mosaic-zone")[1].select("div > a"):
            title = data.select(".jobTitle > span")[0]
            compName = data.select(".companyName")[0]
            companyLocation = data.select(".companyLocation")[0]
            linkJob = this.linkPortalJob + data.get("href")
            
            jobs = {
              "title": title.text,
              "compName": compName.text,
              "companyLocation": companyLocation.text,
              "linkJob": linkJob,
            }
            
            this.listJobs.append(jobs)        
      except:
        print("error looping") 
      
      dumpListJobs = json.dumps(this.listJobs)
      writeJobs = open("jobs.json", "w")
      writeJobs.write(dumpListJobs)
    
  def readFileJobs(self):
    readJobs = open("jobs.json", 'r')
    loadReadJobs = json.load(readJobs)
    
    print(len(loadReadJobs))  
  
scrapingPortalJob = ScarpingPortalJob()
scrapingPortalJob.typingWhat()
scrapingPortalJob.typingWhere()
scrapingPortalJob.clickFindJob()
time.sleep(3)
scrapingPortalJob.recordWeb()
scrapingPortalJob.readFileJobs()

