import pyodbc
import pandas as pd
import requests,json
import sqlalchemy,datetime

# engine = sqlalchemy.create_engine("mssql+pyodbc://sa:password@LAPTOP-IFK6D8L3\\SQLEXPRESS/Bse_Results?driver=SQL+Server")
# df = pd.DataFrame([(i, f'Name{i}') for i in range(1000)], columns=['id', 'name'])  # Example data

# df.to_sql("your_table", engine, if_exists="append", index=False, method="multi", chunksize=500)

# webURL = "https://api.upstox.com/v2/historical-candle/NSE_EQ/1minute/:2025-04-25/:2023-04-25"


url = "https://api.upstox.com/v3/historical-candle/NSE_EQ%7CINE144J01027/minutes/1/2022-01-09"
payload={}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

jsonText = json.loads(response.text)
# FormatJson =list(map(lambda x:str(x).replace('+05:30',''),jsonText['data']['candles']))
# FormatJson =list(map(lambda x:str(x).replace('T',' '),FormatJson))
# FormatJson =list(map(lambda x:str(x).replace("'", ""),FormatJson))
# FormatJson =list(map(lambda x:str(x).split(','),FormatJson))

df_StockQuote = pd.DataFrame(jsonText['data']['candles'],columns=['Datetime','Open','High','Low','Cls','Vol','OI'])
# df_StockQuote[['Datetime','Open','High','Low','Cls','Vol','OI']] = df_StockQuote['Records'].str.split(',',expand=True)
# df_StockQuote['Datetime'] = df_StockQuote['Datetime'].astype('datetime64[s]')
# df_StockQuote['Open'] = df_StockQuote['Open'].values.astype(float)
df_StockQuote['Datetime'] = df_StockQuote['Datetime'].apply(lambda x: datetime.datetime.strptime(str(x)[:-6], '%Y-%m-%dT%H:%M:%S'))
df_StockQuote['Open'] = df_StockQuote['Open'].apply(lambda x: float(x))
df_StockQuote['High'] = df_StockQuote['High'].astype(float)
df_StockQuote['Low'] = df_StockQuote['Low'].astype(float)
df_StockQuote['Cls'] = df_StockQuote['Cls'].astype(float)
df_StockQuote['Vol'] = df_StockQuote['Vol'].astype('Int64')
df_StockQuote['Script_Name'] = '20MICRONS'
df_StockQuote['ISIN'] = 'INE144J01027'
df_StockQuote.columns = ['DateTime','Open','High','Low','Close','Vol','OI','Script_Name','ISIN']
df_StockQuote = df_StockQuote.drop(columns=['OI'])
df_StockQuote = df_StockQuote[['Script_Name','ISIN','DateTime','Open','High','Low','Close','Vol']].reset_index(drop=True)

print(df_StockQuote)
