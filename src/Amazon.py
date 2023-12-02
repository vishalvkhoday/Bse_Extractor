import allure
import allure_pytest
import pytest
from DB_Operation import DB_Operation
from selenium.webdriver.common.action_chains import ActionChains
from Selenium_GridHub import *    # uncomment when executed on remote
# import Selenium_GridHub 
import time
import logging
import pyodbc

logging.getLogger(__name__)

browChrome = Driver
Driver.get("https://www.amazon.in/dp")

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;DATABASE=Bse_Results;UID=sa;PWD=password')
cur = conn.cursor()
import time
time.sleep(2)
while(True):

    sql_SelectPro = "select top 1 [ASIN],Product + [Product Line] as ProductName   from AmazonProductList where ToExecute='Yes' and IsLocked='No'"
    cur.execute (sql_SelectPro)
    ProductName =  cur.fetchone()
    sqlLockRec = "update AmazonProductList set IsLocked='Yes' where ASIN = '{}'".format(ProductName[0])
    cur.execute(sqlLockRec)
    cur.commit()
    logging.info(ProductName)
    browChrome.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]').clear()
    browChrome.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]').send_keys(f"{ProductName[1]}")
    action = ActionChains(browChrome)
    action.send_keys(Keys.ENTER).perform()
    partialName = str(ProductName[1]).split()
    # price = browChrome.find_element(By.XPATH,'//span[@class="a-price"]/span[1]').get_attribute('innerText')
    try:
        price = browChrome.find_element(By.XPATH,f"//span[contains(text(),'{partialName[0]}')]/../../../../div[4]").get_attribute('innerText')
        
        intPrice = str(price).split('₹')
        intPrice = str(intPrice[1]).replace('\n','').replace(',','')
        sqlPrice = f"update AmazonProductList set Price ={intPrice} where ASIN = '{ProductName[0]}' "
        cur.execute(sqlPrice)
        cur.commit()
        sqlToExecute = f"update AmazonProductList set ToExecute='No' where ASIN = '{ProductName[0]}' "
        cur.execute(sqlToExecute)
        cur.commit()
    except:
        cur.rollback()
    
    logging.info(sqlLockRec)

