'''
Created on Sep 5, 2020

@author: DELL
'''
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def getRemoteBrowser():
    Options = ChromeOptions()
    Options.add_argument("start-maximized")
    Options.add_argument("headless")
    Options.add_argument("disable-infobar")
#     Options.add_argument("--incognito")
    
    try:
        #     hubURL="http://192.168.1.102:4444/wd/hub"
#         BrwChrome = webdriver.Remote(command_executor=f"http://192.168.1.113:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME,  options=Options)
        BrwChrome = webdriver.Remote(command_executor=f"http://localhost:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME,  options=Options)
    except:
        BrwChrome =Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", options=Options)
    
    return BrwChrome
    
Driver =getRemoteBrowser()


# # Driver.get_screenshot_as_png()
# print(Driver.title)
# print("Done")


