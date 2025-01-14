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
    session = random.randint(1750021,99999999)
    url ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}&_='
    url = url+ str(session)
    # url ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}'
    headers = {'Accept': 'application/json' ,':method': 'GET'}
    try:
        res =requests.get(url=url)
        stcode = res.status_code
    except Exception as e:
        continue    
    if stcode == 200:
        # print(res.text)
        sRes = res.text        
        try:
            # with open('C:\\Test\Data_1.txt','w') as f:
            #     f.write(sRes)
            sResJson = json.loads(sRes)
        except Exception as e:
            print(e)
            # with open('C:\\Test\Data_1.txt','w') as f:
            #     f.write(sRes)
            time.sleep(1)
            continue
        
        # Niftyticker = fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),sResJson)
        Niftyticker = list(fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),sResJson["data"]))
        
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

        iRant = random.randint(75,100)
        for i in range(iRant,-1,-1):
            print("Next refresh in {} seconds".format(i), end = "\r")
            time.sleep(1)


    