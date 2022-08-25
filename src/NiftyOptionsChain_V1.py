
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import DesiredCapabilities
from select import select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from time import sleep
from pytest import fixture
import allure
import allure_pytest

from MSSQL_Operation import DB_Operation


Options =ChromeOptions()
# Options.add_argument('--start-in-incognito')
Options.add_argument('start-maximized')
# Options.add_argument("--disable-extensions")
chromeBrow = Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver",options=Options,service=None)

arrWin =chromeBrow.window_handles
if len(arrWin)>1:
    chromeBrow.switch_to_window(arrWin[1])
    chromeBrow.close()
    chromeBrow.switch_to_window(arrWin[0])
chromeBrow.get("https://www.moneycontrol.com/indices/fno/view-option-chain/NIFTY/2022-08-11")
sleep(1)
chromeBrow.refresh()
strSpotPrice = chromeBrow.find_element(By.XPATH,'//*[@id="optspotprice"]').get_attribute('innerText')

strSpotPrice = strSpotPrice.replace('Spot Price : ','')
intRow=0
for arrRow in range(0,120):
    strOptxpath ='//*[@id="calls_puts_{}"]'.format(arrRow)
    row_Option = chromeBrow.find_element(By.XPATH,strOptxpath).get_attribute('innerText')
    arrOptions = row_Option.split("\t")
    print(arrOptions)
    for iCell in arrOptions:
        arrCell =iCell.split('\n')
        if len(arrCell)>1:
            pass
        else:
            


