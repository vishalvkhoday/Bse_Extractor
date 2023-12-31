import pandas as pd
import pyodbc
from datetime import datetime


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=StockQuote;UID=sa;PWD=password')

cur = conn.cursor()

IndScript = "select * from Index_Stock where Index_Name = 'Nifty200'"

cur.execute(IndScript)
Nifty200Scr =cur.fetchall()

pdNifty200Script = pd.DataFrame(data=Nifty200Scr)
print(pdNifty200Script)

for r in range(0,len(pdNifty200Script)):
    print(pdNifty200Script[0][r][0])
    scrName = str(pdNifty200Script[0][r][0]).strip()

    sqlScr = f"select * from Actual_NSE_EOD where Script_Name = '{scrName}'"
    cur.execute(sqlScr)
    allRow = cur.fetchall()
    print(allRow)
    cols = ['Script_Name', 'Open', 'High', 'Low', 'Close', 'Volume', 'Pre_Close', 'Change', 'Trnx_date']
    
    scriptPd = pd.read_sql(sqlScr,conn)
    print(scriptPd)
    fName = f"C:\\Nifty200\\{scrName}.csv"
    scriptPd.to_csv(fName,date_format='%Y-%m-%d',index=False)


