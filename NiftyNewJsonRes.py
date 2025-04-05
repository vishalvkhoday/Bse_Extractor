import requests
import fnc,pandas as pd
import time
import random
import json
import pyodbc

def DBCursor():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=Bse_Results;UID=sa;PWD=password')
    cur = conn.cursor()
    return cur

while True:
    cur = DBCursor()
    url ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}&_='
    session = current_timestamp = int(time.time())
    url = url+ str(session)
    # url ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}'
    headers = {'Accept': 'application/json' ,':method': 'GET'}
    try:
        res =requests.get(url=url)
        stcode = res.status_code
    except Exception as e:
        print(e)
        time.sleep(1)
        continue    
    if stcode == 200:
        # print(res.text)
        sRes = res.text        
        try:           
            sResJson = json.loads(sRes)
        except Exception as e:
            print(e)
            time.sleep(1)
            continue
        
        # Niftyticker = fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),sResJson)
        Niftyticker = list(fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),sResJson["data"]))
        dfIndex = pd.DataFrame(Niftyticker,columns=['indexName','timeVal','last','percChange','open','high','low','previousClose'])
        dfIndex = dfIndex[dfIndex['previousClose'] != '-']
        # dfIndex = dfIndex[dfIndex(['last','percChange','open','high','low','previousClose']).apply(lambda x: x.replace(',',''))]
        Niftyticker = dfIndex.values.tolist()
        for i in Niftyticker:
            # i = list(map(lambda x: str(x).replace(',',''),i))
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

        iRant = random.randint(59,80)
        cur.close()
        for i in range(iRant,-1,-1):            
            print("Next refresh in {} seconds   ".format(i), end = "\r")
            time.sleep(1)


    