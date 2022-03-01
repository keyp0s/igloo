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

class timetable:
    #declaring constants
    USERNAME_ID = 'iwpSidebarPortlet|-1|null|tbUsername'
    PASSWORD_ID = 'iwpSidebarPortlet|-1|null|tbPassword'
    TABLE_CLASS = 'iwpTimetableGrid'

    def __init__(self, username, password, directory):
        self.username = username
        self.password = password
        self.directory = directory

    #scrapes the data
    def scrape(self):
        #sets parameters for chrome driver
        chrome_service = Service(self.directory)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get('https://portal.stpiusx.nsw.edu.au/igloo/portal/')

        #function to check whether the page is loaded
        def load_status(element_type,id_name):
            element_present = EC.presence_of_element_located((element_type, id_name))
            WebDriverWait(driver, 10).until(element_present)

        try:
            load_status(By.ID, timetable.USERNAME_ID)

            username = driver.find_element(By.ID, timetable.USERNAME_ID)
            password = driver.find_element(By.ID, timetable.PASSWORD_ID)

            username.send_keys(self.username)
            password.send_keys(self.password)
            password.send_keys(Keys.ENTER)

            try:
                load_status(By.CLASS_NAME, timetable.TABLE_CLASS)
                raw_html = driver.find_element(By.CLASS_NAME, timetable.TABLE_CLASS)

                return (raw_html.get_attribute("outerHTML")) 
                driver.close()

            except:
                #exits if page takes over 10 seconds to load
                print("portal login timeout exception")
                driver.close()
        except:
            #exits if page takes over 10 seconds to load
            print("portal page load timeout exception")
            driver.close()

    #converts raw html to json table
    def format(raw_html):
        raw_table = [[cell.text for cell in row("td")] for row in BeautifulSoup(raw_html,"lxml")("tr")]

        for i in range(len(raw_table)):
            del raw_table[i][6],raw_table[i][2]

        return json.dumps(raw_table,indent=4)


#example code

#load credentials from info.py file
INFO = timetable(info.creds()[0], info.creds()[1], info.creds()[2])

#or load credentials directly
#INFO = timetable(<username>, <password>, <directory>)

#scrape the timetable data
raw_html = timetable.scrape(INFO)

#convert to json
json_table = timetable.format(raw_html)

print(json_table)
