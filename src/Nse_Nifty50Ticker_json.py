'''
Created on Sep 20, 2020

@author: DELL
'''

from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
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
import json
import ast

# def ChBrowser():
#     Options = ChromeOptions()
#     Options.add_argument("start-maximized")
# #     Options.add_argument("headless")
#     Options.add_argument("disable-infobar")
#     #     Options.add_argument("--incognito")
#     ChromeBwr =webdriver.Chrome(executable_path="C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver", chrome_options=Options)
#     return ChromeBwr

    
def test_Nifty():
    
    Options = ChromeOptions()
    Options.add_argument("start-maximized")
    # Options.add_argument("headless")
    # Options.add_argument("disable-infobar")
    # Options.add_argument("user-data-dir=C:/Users/DELL/AppData/Local/Google/Chrome/User Data/Profile 2")
    # Options.add_argument("--incognito")
        
    # ChromeBwr =webdriver.Chrome(chrome_options=Options,executable_path="WebDriver/chromedriver_235", service_args=["--verbose", "--log-path=WebDriver/qc1.log","w+"])
    ChromeBwr =webdriver.Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver", chrome_options=Options)
    arrWin =ChromeBwr.window_handles
    if len(arrWin)>1:
        ChromeBwr.switch_to_window(arrWin[1])
        ChromeBwr.close()
        ChromeBwr.switch_to_window(arrWin[0])
    #     ChromeBwr.get("https://www.nseindia.com/market-data/live-market-indices")
    try:
        ChromeBwr.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/liveIndexWatchData.json")
        # ChromeBwr.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/live_index_watch.htm")
        #     WebDriverWait(ChromeBwr,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="liveIndexWatch"]/tbody/tr[2]')), "Clicked on Home icon")
        while True:
            try:
                tblExist=ChromeBwr.find_element_by_xpath('/html/body/pre').get_attribute('innerText')
                tblExist = str(tblExist).replace('{"data":[','').replace(']}', '')
                dict_List =ast.literal_eval(tblExist)
            except Exception as e:
                print(e)
            
            for item in dict_List:
                
                Script_Name = item.get("indexName")
                DtTm = item.get("timeVal")
                SpotPrice = item.get("last")
                SpotPrice = SpotPrice.replace(',','')
                chg = item.get("percChange")
                chg =chg.replace(',','')
                IndOpen=item.get("open")
                IndOpen=IndOpen.replace(',','')
                IndHigh=item.get("high")
                IndHigh=IndHigh.replace(',','')
                IndLow=item.get("low")
                IndLow=IndLow.replace(',','')
                IndPreClose=item.get("previousClose")
                IndPreClose=IndPreClose.replace(',','')
                strdt= " convert(datetime,'"+str(DtTm)+"')"                
                
                sql_insertQuery = "insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ('{}',{},'{}','{}','{}','{}','{}','{}')".format(Script_Name,strdt,SpotPrice,chg,IndOpen,IndHigh,IndLow,IndPreClose)
                
                conn = DB_Operation().db_ConnectionObject()
                try:
                    print(sql_insertQuery)
                    DB_Operation().Insert_data(conn,sql_insertQuery)
                    DB_Operation().sqlCommit(conn)
                except:
                    DB_Operation().sqlRollBack(conn)
                    
            for i in range(0,43):
                
                print("*"*i, end = "\r")
                sleep(1)
                
            ChromeBwr.refresh()
            sleep(2)
                
    except Exception as e:
        print(e)
        ChromeBwr.refresh()
                    
                 
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    test_Nifty()
    
