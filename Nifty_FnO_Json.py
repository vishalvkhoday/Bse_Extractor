import requests
import pandas as pd
import fnc
import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import json
import pyodbc,time,random


Options = ChromeOptions()
Options.add_argument("start-maximized")
ChromeBwr =webdriver.Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver", chrome_options=Options)


# url = "https://www.nseindia.com/api/equity-stock?index=allcontracts"
# url = "https://www.nseindia.com/api/equity-stock?index=opt_nifty50"
# url = 'https://www.nseindia.com/api/equity-stock?index=opt_niftybank'
        

def getFnOData():
    try:
        res = ChromeBwr.find_element(By.XPATH,"/html/body/pre")
    except:
        ChromeBwr.refresh()
        time.sleep(1)
        res = ChromeBwr.find_element(By.XPATH,"/html/body/pre")

    jsonRes = json.loads(res.text)
    vol_timestamp = jsonRes['vol_timestamp']

    dfFutures = pd.DataFrame(data=jsonRes['value'])
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

url = "https://www.nseindia.com/api/equity-stock?index=opt_nifty50"
ChromeBwr.get(url)

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
