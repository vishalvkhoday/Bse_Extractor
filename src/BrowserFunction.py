'''
Created on Nov 6, 2020

@author: DELL
'''

from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

import pytest
from time import sleep
from pytest import fixture
from DB_Operation import DB_Operation
from time import sleep
from pytest import fixture


def ChBrowser():
    Options = ChromeOptions()
    Options.add_argument("start-maximized")
#     Options.add_argument("headless")
    Options.add_argument("disable-infobar")
    #     Options.add_argument("--incognito")
    ChromeBwr =webdriver.Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", chrome_options=Options)
    return ChromeBwr

