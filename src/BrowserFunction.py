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
    try:
        WebOptions = webdriver.ChromeOptions()
        WebOptions.add_argument("start-maximized")
        WebOptions.add_argument("disable-infobars")
#         driver = webdriver.Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", options=WebOptions,service_args=["--verbose", "--log-path=../../Log/ExecutionLogs.log"])
        driver = webdriver.Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", chrome_options=WebOptions,service_args=["--verbose", "--log-path=../../Log/ExecutionLogs.log"])
        return driver
    except Exception as e:
        print(e)
        assert False

