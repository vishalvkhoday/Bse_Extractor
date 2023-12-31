import json
import pandas as pd
import os
import functools
import itertools

def funcOptiontype(n):
    
    if str(n).find('CE')>0:
        return 'CALL'
    else:
        return 'PUT'

dfNifty = pd.read_json('C:/Stock/NiftyOptionsChain.json')
# dfNifty = pd.read_html('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY')
expDates = list(dfNifty['records'][0])
expDates = expDates[:2]
# print(dfNifty)
All_Rec = []
for row in dfNifty['records'][1]:
    OptType = list(row.keys())
    OptType = OptType[2:]
    
    for Ot in OptType:
        # print(row[Ot],"\n************************\n")
        All_Rec.append(row[Ot])
    
dfNiftyV1 = pd.DataFrame(data=All_Rec)
dfNiftyV1 = dfNiftyV1[dfNiftyV1['expiryDate'].isin(expDates)]
dfNiftyV1 = dfNiftyV1[dfNiftyV1['changeinOpenInterest']!=0]
dfNiftyV1 = dfNiftyV1[(dfNiftyV1['strikePrice']>= dfNiftyV1['underlyingValue']-400) & (dfNiftyV1['strikePrice']<= dfNiftyV1['underlyingValue']+400)]
dfNiftyV1.dropna(axis=0,inplace=True)
dfNiftyV1['OptionType'] = dfNiftyV1['identifier'].apply(funcOptiontype)
dfNiftyV1.to_csv('C:/Stock/NiftyOptionsChain.csv',index=False)
print('done')