import time
from tkinter import StringVar
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import os

#Json read
def read_file(path):
    with open(path, "r") as rf:
        values = json.load(rf)
    return values
#json values#
property_json = read_file('settings.json')


IP = StringVar()
IP.set(property_json['TesterInfo']['TesterIP'])


driver  = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get('http://localhost:5001/v6.15.8.html')
time.sleep(10)

driver.find_element(By.XPATH,"//span[@class='rc-select-selection__clear']").click()
driver.find_element(By.XPATH,"//input[@class='rc-select-search__field']").send_keys('192.168.4.90')
driver.find_element(By.XPATH,"//button[@class='grl-connect-button grl-button connectionsetup-leftsideSetWidth btn btn-primary']").click()
time.sleep(10)
