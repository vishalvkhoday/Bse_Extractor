import requests
import fnc
import time
import random
import json
import pyodbc
import pytest
from selenium.webdriver.chrome.service import Service


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=Bse_Results;UID=sa;PWD=password')
cur = conn.cursor()
while True:
    url ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}'
    # url ='https://www.nseindia.com/api/allIndices'
    try:
        res =requests.get(url=url)
        stcode = res.status_code
    except Exception as e:
        continue    
    if stcode == 200:
        # print(res.text)
        sRes = res.text
        sRes = sRes.replace('\r\n','')
        # sRes = sRes.replace('{"data":','')
        sRes = sRes.replace('{  "data":','')
        sRes = sRes[:-1]
        sResJson = json.loads(sRes)
        
        Niftyticker = list(fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),sResJson))
        
        for i in Niftyticker:
            print(i)
            Ind = i[0]
            Trd = i[1]
            Spot = str(i[2]).replace(',','')
            Chg = i[3]
            IndOpen = i[4].replace(',','')
            IndHigh = i[5].replace(',','')
            IndLow = i[6].replace(',','')
            IndPreCls = i[7].replace(',','')
           
            NiftySql = f"insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ( '{Ind}',CONVERT(datetime,'{Trd}'),'{Spot}','{Chg}','{IndOpen}','{IndHigh}','{IndLow}','{IndPreCls}')"
            print(NiftySql)
            try:
                cur.execute(NiftySql)
                cur.commit()
            except Exception as e:
                print(e)

        iRant = random.randint(30,70)
        for i in range(iRant,-1,-1):
            print("Next refresh in {} seconds".format(i), end = "\r")
            time.sleep(1)


    