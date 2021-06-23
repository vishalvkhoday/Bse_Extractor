'''
Created on Sep 20, 2020

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
from BrowserFunction import *
import pytest
from time import sleep
from pytest import fixture
from DB_Operation import DB_Operation
from time import sleep
from pytest import fixture


# def ChBrowser():
#     Options = ChromeOptions()
#     Options.add_argument("start-maximized")
# #     Options.add_argument("headless")
#     Options.add_argument("disable-infobar")
#     #     Options.add_argument("--incognito")
#     ChromeBwr =webdriver.Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", chrome_options=Options)
#     return ChromeBwr

    
def test_Nifty():
    while True:
        Options = ChromeOptions()
        Options.add_argument("start-maximized")
        # Options.add_argument("headless")
        Options.add_argument("disable-infobar")
        # Options.add_argument("user-data-dir=C:/Users/DELL/AppData/Local/Google/Chrome/User Data/Profile 2")
        # Options.add_argument("--incognito")
            
        ChromeBwr =webdriver.Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", chrome_options=Options)
        arrWin =ChromeBwr.window_handles
        if len(arrWin)>1:
            ChromeBwr.switch_to_window(arrWin[1])
            ChromeBwr.close()
            ChromeBwr.switch_to_window(arrWin[0])
        #     ChromeBwr.get("https://www.nseindia.com/market-data/live-market-indices")
        try:
            # ChromeBwr.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/liveIndexWatchData.json")
            ChromeBwr.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/live_index_watch.htm")
            #     WebDriverWait(ChromeBwr,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="liveIndexWatch"]/tbody/tr[2]')), "Clicked on Home icone")
            tblExist=ChromeBwr.find_element_by_xpath('//*[@id="liveIndexWatch"]/tbody/tr[2]')
            ActionChains(ChromeBwr).key_down(Keys.ESCAPE).perform()
        except:
            ActionChains(ChromeBwr).key_down(Keys.ESCAPE).perform()
            ActionChains(ChromeBwr).key_down(Keys.ESCAPE).perform()
            ActionChains(ChromeBwr).key_down(Keys.ESCAPE).perform()
            print("Escape key pressed")
    #     tblExist.send_keys(Keys.ESCAPE)
    # #     rowCount = ChromeBwr.find_element_by_xpath('//*[@id="liveindexTable"]/tbody').get_attribute("childElementCount")
        rowCount = 28
       
        conn = DB_Operation().db_ConnectionObject()
        for row in range(3,int(rowCount)):
    #         row_xpath = '//*[@id="liveindexTable"]/tbody/tr[{}]'.format(int(row))
            row_xpath = '//*[@id="liveIndexWatch"]/tbody/tr[{}]'.format(int(row))
            rowVal = ChromeBwr.find_element_by_xpath(row_xpath).get_attribute("innerText")
            rowVal =rowVal.replace(",","")
            colVal = rowVal.split("\t")
            
            if len(colVal)>1:
                try:
                    sql_insertQuery = "insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ('{}',getdate(),'{}','{}','{}','{}','{}','{}')".format(colVal[0],colVal[1],colVal[2],colVal[3],colVal[4],colVal[5],colVal[6])
                    
                    print(sql_insertQuery)
                    DB_Operation().Insert_data(conn,sql_insertQuery)
                except:
                    DB_Operation().sqlRollBack(conn)
                    
            DB_Operation().sqlCommit(conn)
            print (rowVal)
        
                    
        ChromeBwr.quit()         
        sleep(52)
