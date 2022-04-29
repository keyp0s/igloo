from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import info
import json

class Igloo:
    #declaring constants
    USERNAME_ID = 'iwpSidebarPortlet|-1|null|tbUsername'
    PASSWORD_ID = 'iwpSidebarPortlet|-1|null|tbPassword'
    TIMETABLE = '__portlet|2|-306|dgMain'
    ASSESSMENT = '__portlet|2|-305|dgMain'
    HOMEWORK = '__portlet|2|-318|dgMain'

    #scrapes the data
    def scrape(username, password, directory, element):
        #sets parameters for chrome driver
        chrome_service = Service(directory)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get('https://portal.stpiusx.nsw.edu.au/Igloo/portal/')
        
        #function to check whether the page is loaded
        def load_status(element_type,id_name):
            element_present = EC.presence_of_element_located((element_type, id_name))
            WebDriverWait(driver, 10).until(element_present)

        try:
            load_status(By.ID, Igloo.USERNAME_ID)

            username_id = driver.find_element(By.ID, Igloo.USERNAME_ID)
            password_id = driver.find_element(By.ID, Igloo.PASSWORD_ID)
            
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
    def timetable(raw):
        raw = [[cell.text for cell in row("td")] for row in BeautifulSoup(raw,"lxml")("tr")]

        for i in range(len(raw)):
            del raw[i][6],raw[i][2]

        return json.dumps(raw)

    def homework(raw):
        raw = [[cell.text for cell in row("td")] for row in BeautifulSoup(raw,"lxml")("tr")]

        for i in range(len(raw)):
            del raw[i][3]

        return json.dumps(raw)

    def assessment(raw):
        raw = [[cell.text for cell in row("td")] for row in BeautifulSoup(raw,"lxml")("tr")]
        
        for i in range(len(raw)):
            del raw[i][4]

        return json.dumps(raw)


#example code

#load credentials from info.py file
INFO = [info.creds()[0], info.creds()[1], info.creds()[2]]

#or load credentials directly
#INFO = [<username>, <password>, <directory>]

#Igloo the data from Igloo
raw_html = Igloo.scrape(*INFO,[Igloo.TIMETABLE,Igloo.HOMEWORK,Igloo.ASSESSMENT])

#convert raw html to json

#convert timetable
timetable = Igloo.timetable(raw_html[0])
print(timetable)

#convert homework
homework = Igloo.homework(raw_html[1])
print(homework)

#convert assessment
assessment = Igloo.assessment(raw_html[2])
print(assessment)