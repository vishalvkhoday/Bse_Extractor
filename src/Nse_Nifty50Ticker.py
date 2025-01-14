'''
Created on Sep 20, 2020

@author: DELL
'''

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from BrowserFunction import *
import pytest
from time import sleep
from pytest import fixture
from DB_Operation import DB_Operation
from selenium.webdriver.chrome.service import Service


Options = ChromeOptions()
Options.add_argument("start-maximized")
# Options.add_argument("headless")
Options.add_argument("disable-infobar")
# serviceObj = Service('C:/Users/Vishal/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
serviceObj = Service('C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver.exe')
browChrome =  webdriver.Chrome(service=serviceObj,options=Options)
sleep(2)
def test_Nifty():
    while True:
                
        # browChrome = webdriver.Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver", chrome_options=Options) #Driver
        try:
            browChrome.get("https://www.nseindia.com/api/allIndices")
            str_all_data = browChrome.find_element(By.XPATH,"/html/body/pre")
            sleep(45)
        except Exception as e:
            print(e)
            sleep(1)
            continue

test_Nifty()