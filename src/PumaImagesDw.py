from  selenium import webdriver
import pytest
import selenium.webdriver.common.by
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
import requests
from  selenium.webdriver.common.keys import Keys
import time

# Change file path here 
def readExcel():
    xlSheet = pd.read_excel('C:\Amazon\Puma-article code.xlsx',sheet_name='Sheet1')
    xlPd =pd.DataFrame(data=xlSheet)
    # xlPd = xlPd.loc[xlPd['ToExecute'] == 'Yes']    
    return xlPd


def ImagDw(PCode):    
    ArticalCode = f"Puma {PCode}"
    filpDriver.find_element(By.NAME,'q').clear()
    filpDriver.find_element(By.NAME,'q').send_keys(ArticalCode)
    filpDriver.find_element(By.NAME,'q').send_keys(Keys.ENTER)
    location = 'c:/Amazon/'
    
    
    filpDriver.find_element(By.XPATH,'(//a/div/img)[1]').click()
    time.sleep(1)
    iCounter=1
    for x in range(1,4):
        imglocs = filpDriver.find_elements(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')
        # imglocs = filpDriver.find_elements(By.XPATH,'//div[@data-lhcontainer="1"]/div/div[3]/div[1]/a/img')
        for imgs in imglocs:
            # imglocs = filpDriver.find_element(By.XPATH,imgloc)
            imgloc =imgs.get_attribute('src')
            print(imgloc)
            if imgloc.find('https://') >=0 :
                with open (f'{location}{PCode}_{iCounter}.png','wb') as f:
                    f.write(requests.get(imgloc).content)
                    iCounter = iCounter+1
                    filpDriver.find_element(By.XPATH,'(//*[@class="t0PEec"])[1]').click()
                    time.sleep(1)
    

Options = webdriver.ChromeOptions()
Options.add_argument("--start-maximized")

# service = Service(executable_path="D:/flipkart/chromedriver.exe")
service = Service(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver")

filpDriver = webdriver.Chrome(service=service)


if __name__ == '__main__':
     pdXlxallRec = readExcel()
     filpDriver.get(f"https://www.google.com/imghp")
     filpDriver.maximize_window()
     for iCount,row in pdXlxallRec.iterrows():
        print(iCount)
        if row['ToExecute'] =='Yes':
                
            PCode = row['ProductCode']
            try:
                
                ImagDw(PCode)
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'ToExecute'] = 'No'
                

                
            except Exception as  e:
                print(e)
                # pdXlxallRec.to_excel('C:/Vishal/git/Bse_Extractor/src/AmazonProductList.xlsx',sheet_name='Sheet1',index=False)
                continue


# pdXlxallRec.to_excel('C:/Vishal/git/Bse_Extractor/src/AmazonProductList.xlsx',sheet_name='Sheet1',index=False)
print('Done')
