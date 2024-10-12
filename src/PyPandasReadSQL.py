import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import numpy as np




def connect(**kwargs):
    try:
        connection_string = MSSQLConnectStr(**kwargs)
        return   pyodbc.connect(connection_string)
        # return   pyodbc.connect(connection_string).cursor()
                
    except pyodbc.Error as e:
        print(e)


connectionParms = {
    # "DRIVER":"ODBC Driver 17 for SQL Server",
    # "SERVER":"LAPTOP-IFK6D8L3\\SQLEXPRESS",
    "DATABASE":"StockQuote",
    # "UID":"sa",
    # "PWD":"password"
}

NSE = "select top 10 * from NSE_EOD where script_name = '20MICRONS' order by 9 desc"
BSE = "select top 10 * from Nifty_Ticker"
DB =connectionParms.get("DATABASE")
SQL = lambda DB:NSE if DB.find("StockQuote") >= 0 else BSE
print(SQL(DB))
MSSQLConnect = connect(**connectionParms)
dfSQL = pd.read_sql(SQL(DB),MSSQLConnect)
dfSQL['SQ']= dfSQL['Open'].apply(np.max).round(2)
print(dfSQL)
