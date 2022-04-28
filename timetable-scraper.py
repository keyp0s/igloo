from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import info
import json

class scrape:
    #declaring constants
    USERNAME_ID = 'iwpSidebarPortlet|-1|null|tbUsername'
    PASSWORD_ID = 'iwpSidebarPortlet|-1|null|tbPassword'
    TABLE_ID = '__portlet|2|-306|dgMain'
    ASSESSMENT_ID = '__portlet|2|-305|dgMain'
    HOMEWORK_ID = '__portlet|1|-318|dgMain'

    def __init__(self, username, password, directory):
        self.username = username
        self.password = password
        self.directory = directory

    #scrapes the data
    def scraper(username, password, directory, element):
        #sets parameters for chrome driver
        chrome_service = Service(directory)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get('https://portal.stpiusx.nsw.edu.au/igloo/portal/')
        
        #function to check whether the page is loaded
        def load_status(element_type,id_name):
            element_present = EC.presence_of_element_located((element_type, id_name))
            WebDriverWait(driver, 10).until(element_present)

        try:
            load_status(By.ID, scrape.USERNAME_ID)

            username_id = driver.find_element(By.ID, scrape.USERNAME_ID)
            password_id = driver.find_element(By.ID, scrape.PASSWORD_ID)
            
            username_id.send_keys(username)
            password_id.send_keys(password)
            password_id.send_keys(Keys.ENTER)
            try:
                items = []
                for item in element:
                    load_status(By.ID, item)
                    raw_html = driver.find_element(By.ID, item)
                    items.append(raw_html.get_attribute("outerHTML"))

                return items
                driver.close()

            except Exception as err:
                #exits if page takes over 10 seconds to load
                print("possible page load timeout, raised exception:",err)
                driver.close()
        except Exception as err:
            #exits if page takes over 10 seconds to load
            print("possible page load timeout, raised exception:",err)
            driver.close()

#converts raw html to json table
class format:
    def __init__(self, raw):
        self.raw = raw
    def timetable(self):
        raw_table = [[cell.text for cell in row("td")] for row in BeautifulSoup(self.raw,"lxml")("tr")]

        for i in range(len(raw_table)):
            del raw_table[i][6],raw_table[i][2]

        return json.dumps(raw_table,indent=4)

    def homework(self):
        raw_table = [[cell.text for cell in row("td")] for row in BeautifulSoup(self.raw,"lxml")("tr")]

        for i in range(len(raw_table)):
            del raw_table[i][2]

        return json.dumps(raw_table,indent=4)


#example code

#load credentials from info.py file
INFO = [info.creds()[0], info.creds()[1], info.creds()[2]]

#or load credentials directly
#INFO = [<username>, <password>, <directory>]

#scrape the data from igloo
raw_html = scrape.scraper(*INFO,[scrape.TABLE_ID,scrape.HOMEWORK_ID])

#convert to json

#convert timetable
RAW_TIMETABLE = format(raw_html[0])
timetable = format.timetable(RAW_TIMETABLE)
print(timetable)

#convert homework
RAW_HOMEWORK = format(raw_html[1])
homework = format.homework(RAW_HOMEWORK)
print(homework)



