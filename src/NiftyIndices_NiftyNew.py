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
import fnc
import random
import datetime
from selenium.webdriver.chrome.service import Service


Options = ChromeOptions()
Options.add_argument("start-maximized")
# Options.add_argument("headless")
Options.add_argument("disable-infobar")
serviceObj = Service('C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver.exe')
    
def test_Nifty():    
    ChromeBwr =  webdriver.Chrome(service=serviceObj,options=Options)
    arrWin =ChromeBwr.window_handles
    if len(arrWin)>1:
        ChromeBwr.switch_to.new_window('tab')
        ChromeBwr.close()
        ChromeBwr.switch_to.window('main')
    
    try:
        ChromeBwr.get("https://www.nseindia.com/api/allIndices")
        
        while True:
            try:
                allData = []
                strJson = ChromeBwr.find_element(By.XPATH,'/html/body/pre').get_attribute('innerText')
                jsonAllIndex = json.loads(strJson)
                DtTm = jsonAllIndex["timestamp"]
                Niftyticker = list(fnc.map(('index','last','percentChange','open','high','low','previousClose'),jsonAllIndex["data"]))
                
               
                for x in Niftyticker:
                    print(x)
                    Script_Name = x[0]
                    SpotPrice = str(x[1]).replace(',','')
                    chg = x[2]
                    IndOpen = str(x[3]).replace(',','')
                    IndHigh = str(x[4]).replace(',','')
                    IndLow  = str(x[5]).replace(',','')
                    IndPreClose = str(x[6]).replace(',','')

                    sql_insertQuery = "insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ('{}','{}','{}','{}','{}','{}','{}','{}')".format(Script_Name,DtTm,SpotPrice,chg,IndOpen,IndHigh,IndLow,IndPreClose)
                    conn = DB_Operation().db_ConnectionObject()
                    try:
                        print(sql_insertQuery)
                        DB_Operation().Insert_data(conn,sql_insertQuery)
                        DB_Operation().sqlCommit(conn)
                    except:
                        DB_Operation().sqlRollBack(conn)
                    
                iRant = random.randint(30,70)
                for i in range(iRant,-1,-1):
                    print("Next refresh in {} seconds  ".format(i), end = "\r")
                    sleep(1)
                
                ChromeBwr.refresh()
                sleep(2)

                
            except Exception as e:
                print(e)
                sleep(2)
                ChromeBwr.refresh()
        
    except Exception as e:
        print(e)          
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    test_Nifty()
    
