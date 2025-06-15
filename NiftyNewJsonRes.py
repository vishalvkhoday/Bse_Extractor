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
    webURL ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}&_='+str(int(time.time()))
    # url ='https://iislliveblob.niftyindices.com/jsonfiles/LiveIndicesWatch.json?{}'
    
    header = {'Accept': 'application/json' }
    try:
        res =requests.get(url=webURL,headers=header,timeout=5).json()
        # Niftyticker = list(fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),sResJson["data"]))
        Niftyticker = list(fnc.map(('indexName','timeVal','last','percChange','open','high','low','previousClose'),res["data"]))
        dfIndex = pd.DataFrame(Niftyticker,columns=['indexName','timeVal','last','percChange','open','high','low','previousClose'])
        dfIndex = dfIndex[dfIndex['previousClose'] != '-']
        Niftyticker = dfIndex.values.tolist()
        for i in Niftyticker:
            ii = list(map(lambda x: str(x).replace(',',''),i[2:]))
            # print(i)  
            # NiftySql = f"insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ( '{Ind}',CONVERT(datetime,'{Trd}'),'{Spot}','{Chg}','{IndOpen}','{IndHigh}','{IndLow}','{IndPreCls}')"
            NiftySql = f"""insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values
              ( '{i[0]}',CONVERT(datetime,'{i[1]}'),'{ii[0]}','{ii[1]}','{ii[2]}','{ii[3]}','{ii[4]}','{ii[5]}')"""
            print(NiftySql)
            try:
                cur.execute(NiftySql)
                cur.commit()
            except Exception as e:
                print(e)
                cur.rollback()
    except Exception as e:
        print(e)
    cur.close()
    iRant = random.randint(59,80)
    for i in range(iRant,-1,-1):            
        print("Next refresh in {} seconds   ".format(i), end = "\r")
        time.sleep(1)


    