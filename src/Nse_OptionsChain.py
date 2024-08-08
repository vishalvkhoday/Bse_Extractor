

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from select import select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
import pytest
from time import sleep
from pytest import fixture

from MSSQL_Operation import DB_Operation


while True:
    Options =ChromeOptions()
    Options.add_argument('--start-in-incognito')
    Options.add_argument('start-maximized')
    # Options.add_argument("--disable-extensions")
    # chromeBrow = Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver",options=Options)
    chromeBrow = Chrome(options=Options,service=None,)


    def fnClick(oBrowser):
        for i in range(0,10):
            try:
                objState =oBrowser.is_displayed()

                if objState == True:
                    oBrowser.click()
                    break
            except:
                sleep(1)


    try:
        chromeBrow.get("https://www.nseindia.com/market-data/equity-derivatives-watch")
    except Exception as e:
        print(e)
        chromeBrow.close()
    objDb =DB_Operation()
    sleep(3)
    try:
        strTradDt = chromeBrow.find_element(By.XPATH,'//*[@id="liveEquityDerTimes"]').get_attribute('innerText')
        strTradDt = str(strTradDt).replace('Market is Open As on','')
        strTradDt = str(strTradDt).replace('Market is Closed As on','')
        
        strTradDt = str(strTradDt).replace('IST','').strip()
        strTradDt = strTradDt[:20]
        if len(str(strTradDt).strip())==0:
            chromeBrow.refresh()
    except Exception as e:
        print(e)
        continue
    # print(strTradDt) 
    sleep(3)
    try:
        strOptionData=chromeBrow.find_element(By.ID,"eqderivativesTable").get_attribute('innerText')
    except:
        chromeBrow.close()
        continue
    arrOptionData = str(strOptionData).split('\n')

    for strRow in arrOptionData:
        
        strRow=str(strRow).replace(',','')
        strCell = str(strRow).split('\t')
        
        if len(strCell)==12:
            sInsertSql = "insert into NSE_OptionsChain (Symbol, ExpDate, OptionType, StrikePrice, LastPrice, Chg, chgPercentage, Volume, [Value], OpenInt, UnderLayingValue, TrdDateTime)Values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(strCell[1],strCell[2],strCell[3],strCell[4],strCell[5],strCell[6],strCell[7],strCell[8],strCell[9],strCell[10],strCell[11],strTradDt)
            # print (sInsertSql)
            
            objDb.sql_InsertUpdateAndCommit(sInsertSql)
            
            # DB_Operation.sqlRollBack()


    print("\n\n\n *****************Completed for now*******************")
    chromeBrow.close()
    N=120
    for i in range(N,-1,-1):                
                print("Next refresh in {} seconds".format(i), end = "\r")
                sleep(1)