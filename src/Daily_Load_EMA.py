

import pandas as pd
import scipy
import pyodbc
import csv

import time
import numpy as np


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=StockQuote;UID=sa;PWD=password')
cur = conn.cursor()
DB =  []
with open ('C:/Vishal/git/Bse_Extractor/src/ABB.csv') as csvFile:
    readData =  pd.read_csv('C:/Vishal/git/Bse_Extractor/src/ABB.csv')
    # lastrow =len(readData)
    # spamreader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    # for row in spamreader:
    #     print(', '.join(row))
    ArrNP = readData.to_numpy()
    ArrNP2 = ArrNP[:,3:]
    # print(ArrNP)
    print(np.ndim(ArrNP2))
    print(np.size(ArrNP2))
    print(np.shape(ArrNP2))


arr = np.zeros((3,486,21))
arr[0,:,:]=ArrNP2[:,:]
print(arr)
# for i in range(0,arr.shape[0]):
#     for j in range(0,arr.shape[1]):
#         for k in range(0,arr.shape[2]):
#             arr[i,j,k] = i*j*k

# print(arr)
# print(arr[2,3,4])

