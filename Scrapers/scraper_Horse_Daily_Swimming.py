#import libraries
from bs4 import BeautifulSoup
import requests
import string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import pandas as pd
import os.path
import re

#starting webdriver
#https://racing.hkjc.com/racing/info/latestonhorse/list/english
#https://racing.hkjc.com/racing/info/latestonhorse/swim/list/chinese
BASE_URL = "https://racing.hkjc.com/Racing/Info/MCS/Chinese/horses/swim/"
BASE_URL_SUFFIX = "_000000_S_SWIM.xml.zip"
dates = ["20300701",
  
"20200731",
"20200801",         
"20200802",
"20200803",
"20200804",
"20200805",




]
 

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

def check_exists_by_xpath(xpath):
  try:
      driver.find_element_by_xpath(xpath)
  except NoSuchElementException:
      return False
  return True

"""
Initialize variables: 

Data collected per entry: 
Date, Horse, Trainer, Type, Racecourse/Track, Workouts, Gear
"""
table_row_xpath = "/html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr"



count = 0

# Begin grabbing data
for meet in dates:
  print("Scraping: " + meet)
  race_entry = []
  internalRaceCount = 1
  count += 1
  if os.path.isfile('Daily_Swimming_' + str(meet) + '.txt'):
    continue
  else:
    driver.get(BASE_URL + meet + BASE_URL_SUFFIX)
    driver.implicitly_wait(20)

    # Get BrandNo, Date, Type, Racecourse/Track, Workouts, Gear
  #if (check_exists_by_xpath(table_row_xpath)):
    #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    #table_rows = tempTableEl

  if not (check_exists_by_xpath(table_row_xpath)):
    continue
  else:
    tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    table_rows = tempTableEl

    for row in table_rows:
      rowEntry = []

      rowEntry.append(meet)
 
      cols = row.find_elements_by_tag_name('td')
      for col in cols:
        rowEntry.append(col.text)
      race_entry.append(rowEntry)
     
    # Save file as csv
    df = pd.DataFrame(race_entry)
    print(df.head())
    csv_data = df.to_csv("./Daily_Swimming_" + str(meet) + ".txt", index=False)
    #csv_data = df.to_csv("./Daily_Trackwork_" + str(meet) + ".csv", index=False)
    print("Saved " + str(meet))

driver.quit()
