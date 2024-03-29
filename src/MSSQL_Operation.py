'''
Created on Sep 6, 2020

@author: DELL
'''

# import pymssql
import datetime
from pytest import fixture
import pyodbc
    
# conn = pymssql.connect(user='sa',password='password',host='.\\SQLEXPRESS', database='Bse_Results',port='1433')
# cur=conn.cursor()
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=Bse_Results;UID=sa;PWD=password')

class DB_Operation():

    def __init__(self,sql_Query=""):
        self.sql_Query = sql_Query
       
    
    def db_ConnectionObject(self):
        
        # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=StockQuote;UID=sa;PWD=password')
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=Bse_Results;UID=sa;PWD=password')
        # conn = pymssql.connect(user='sa',password='password',host='LAPTOP-IFK6D8L3\\SQLEXPRESS', database='Bse_Results',port='1433')
        return conn
#         
    
    def db_selectFetchAll(self,sql_Query):
        # conn = DB_Operation.db_ConnectionObject(self)
        cur = conn.cursor()
        cur.execute(sql_Query)
        ret_Row_Val = cur.fetchall()
        # conn.close()
        return ret_Row_Val

    
    def db_selectFetchone(self,sql_Query):
        try:
            # conn = DB_Operation.db_ConnectionObject(self)
            cur = conn.cursor()
            cur.execute(sql_Query)
    #         ret_Row_Val = cur.fetchall()
            ret_Row_Val = cur.fetchone()
            return ret_Row_Val
        except Exception as e:
            print(e+"\n\n")
            print("Could not fetch record")
      
    def InsertUpdate_data(self,sql_Query):
        try:
            # conn = DB_Operation.db_ConnectionObject(self="")
            # conn = objInsert
            cur = conn.cursor()
            cur.execute(sql_Query)
            print("Data inserted {}".format(sql_Query))
            conn.commit()
    #         print("Transaction commited")
            # conn.close()
            print("Transaction commited Connection close")
        except Exception as e:
            print(e)
            conn.rollback
            # conn.close()
    
    
    
    def Update_data(self,sql_Query):
        try:
            # conn = DB_Operation.db_ConnectionObject(self)
            cur =conn.cursor()
            cur.execute(sql_Query)
            conn.commit()
            
            print(sql_Query)
        except Exception as e:
            print(e)
            conn.rollback
            # conn.close()
            
        
        
    def sqlCommit(self):
        try:
            # conn = DB_Operation.db_ConnectionObject(self)
            conn.commit()
            print("Transaction commit successful")
        except Exception as e:
            print(e+"\n\n")
            print("No transaction to rollback")

    def sqlRollBack(self):
        try:
            # conn = DB_Operation.db_ConnectionObject(self)
            conn.rollback()
            print("Transaction rollback successful")
        except Exception as e:
            print(e+"\n\n")
            print("Rollback failed !!!")

    def closeConnection(self):
        conn.close()
    
    
    def sql_InsertUpdateAndCommit(self,sql_Query):
        try:            
            # conn= DB_Operation.db_ConnectionObject(self)
            cur =conn.cursor()
            print("Data inserted {}".format(sql_Query))
            cur.execute(sql_Query)
            conn.commit()
            print("Transcation commit successful\n\n")
        except Exception as e:
            print(e)

conn=DB_Operation.db_ConnectionObject(self="")
