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
import random
import datetime
from selenium.webdriver.chrome.service import Service


Options = ChromeOptions()
Options.add_argument("start-maximized")
# Options.add_argument("headless")
Options.add_argument("disable-infobar")
serviceObj = Service('C:/Users/Vishal/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')



    
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
                allData = 
                TrdDatetime = ChromeBwr.find_element(By.XPATH,'/html/body/pre').get_attribute('innerText')
                curTime = datetime.datetime.now().strftime('%H:%M:%S')
                #cTrdTime = datetime.datetime.strptime(TrdDatetime,'%H:%M:%S').time()

                #print(datetime.datetime.timestamp())
                strdt = str(datetime.date.today())+' '+ str(TrdDatetime)
                # strdt = datetime.datetime.strptime(strdt,'%Y-%m-%d %H:%M:%S %p').now()
                # if strdt <= datetime.datetime.now():
                #     pass
               
                for x in range(1,14):
                    tblExist=ChromeBwr.find_element(By.XPATH,f'//*[@id="stockwatchtable"]/tbody/tr[{x}]').get_attribute('innerText')
                    tblExist = str(tblExist).replace('%','').replace('\t\n\t','\t').replace('\n\t','\t')
                    arrtblExist = tblExist.split('\t')
                    print(tblExist)
                    Script_Name = arrtblExist[0]
                    DtTm = TrdDatetime
                    SpotPrice =str(arrtblExist[4]).replace(',','')
                    chg = arrtblExist[1]
                    IndOpen = str(arrtblExist[7]).replace(',','')
                    IndHigh = str(arrtblExist[5]).replace(',','')
                    IndLow  = str(arrtblExist[3]).replace(',','')
                    IndPreClose = str(arrtblExist[6]).replace(',','')

                    sql_insertQuery = "insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ('{}','{}','{}','{}','{}','{}','{}','{}')".format(Script_Name,strdt,SpotPrice,chg,IndOpen,IndHigh,IndLow,IndPreClose)
                    conn = DB_Operation().db_ConnectionObject()
                    try:
                        print(sql_insertQuery)
                        DB_Operation().Insert_data(conn,sql_insertQuery)
                        DB_Operation().sqlCommit(conn)
                    except:
                        DB_Operation().sqlRollBack(conn)
                    
                iRant = random.randint(30,70)
                for i in range(iRant,-1,-1):
                    print("Next refresh in {} seconds".format(i), end = "\r")
                    sleep(1)
                
                ChromeBwr.find_element(By.XPATH,'//*[@class="refresh"]').click()
                sleep(2)

                
            except Exception as e:
                print(e)
        # ChromeBwr.refresh()
    except Exception as e:
        print(e)          
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    test_Nifty()
    
