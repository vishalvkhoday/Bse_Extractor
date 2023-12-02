
import pandas as pd
import scipy
import pyodbc

import time

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=StockQuote;UID=sa;PWD=password')
cur = conn.cursor()


SQL_NLM_250 = """
select Script_Name,[close] from NSE_EOD where Trnx_date = (select max(Trnx_date) from NSE_EOD)
"""

varNLM250 = cur.execute(SQL_NLM_250)

for i in varNLM250:
    print(i[1])