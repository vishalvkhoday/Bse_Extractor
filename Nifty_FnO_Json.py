import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import json
import pyodbc,time,random
from selenium.webdriver.chrome.service import Service

Options = ChromeOptions()
Options.add_argument("start-maximized")
Options.add_argument("disable-infobars")


serviceObj = Service('C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver.exe')
# browChrome =  webdriver.Chrome(options=Options) #Driver
ChromeBwr =  webdriver.Chrome(service=serviceObj,options=Options) #Driver
# url = "https://www.nseindia.com/api/equity-stock?index=allcontracts"
# url = "https://www.nseindia.com/api/equity-stock?index=opt_nifty50"
# url = 'https://www.nseindia.com/api/equity-stock?index=opt_niftybank'
# ChromeBwr.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY")
# cookies = ChromeBwr.get_cookies()
# for cookie in cookies:
#     ChromeBwr.add_cookie(cookie)
# ChromeBwr.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY")
        

def getFnOData():
    try:
        res = ChromeBwr.find_element(By.XPATH,"/html/body/pre")
    except:
        ChromeBwr.refresh()
        time.sleep(1)
        res = ChromeBwr.find_element(By.XPATH,"/html/body/pre")

    jsonRes = json.loads(res.text)
    vol_timestamp = jsonRes['records']['timestamp']
    
    dfFut = pd.read_json(res.text)
    for y in dfFut.iterrows():
        print(y[1][0])

    dfFutures = pd.DataFrame(data=jsonRes['records']['data'])
    dfFutures['vol_timestamp'] =vol_timestamp

    for i in dfFutures.iterrows():        
        sqlFnO ="INSERT INTO [dbo].[tbl_NseFnODetails] ([underlying],[Identifier] ,[instrumentType]  ,[Instrument]  ,[ExpiryDate] ,[OptionType]  ,[strikePrice]  ,[lastPrice]  ,[pChange] ,[openPrice]  ,[highPrice]  ,[lowPrice] ,[ContractsTraded] ,[openInterest] ,[underlyingValue] ,[vol_timestamp]) "
        fullSql = f"{sqlFnO} VALUES ('{i[1][0]}','{i[1][1]}','{i[1][2]}','{i[1][3]}','{i[1][4]}','{i[1][5]}','{i[1][6]}','{i[1][7]}','{i[1][8]}','{i[1][9]}','{i[1][10]}','{i[1][11]}','{i[1][12]}','{i[1][15]}','{i[1][16]}','{i[1][17]}') "
        print(fullSql)
        try:
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=Bse_Results;UID=sa;PWD=password')
            cur = conn.cursor()
            cur.execute(fullSql)
            cur.commit()
            cur.close()
        except Exception as e:
            print(e)

Weburl = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
ChromeBwr.get(Weburl)

while True:
    
    try:        
        getFnOData()
    except:
        continue
    

    iRant = random.randint(130,170)
    for i in range(iRant,-1,-1):
        print("Next refresh in {} seconds".format(i), end = "\r")
        time.sleep(1)
    ChromeBwr.refresh()
