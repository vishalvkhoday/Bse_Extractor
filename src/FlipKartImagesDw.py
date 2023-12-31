from  selenium import webdriver
import pytest
import urllib3
import urllib
import selenium.webdriver.common.by
from selenium.webdriver.common.by import By
import requests
import pandas as pd

def readExcel():
    xlSheet = pd.read_excel('C:/Users/Vishal/Downloads/fsn 8-6-23 upload.xlsx',sheet_name='Sheet1')
    xlPd =pd.DataFrame(data=xlSheet)
    # xlPd = xlPd.loc[xlPd['ToExecute'] == 'Yes']

    
    return xlPd


def ImagDw(PCode):
    filpDriver.get(f"https://www.flipkart.com/product/p/itme?pid={PCode}")
    imgs = filpDriver.find_elements(By.XPATH,elemxpath)
    
    proPrice = filpDriver.find_element(By.XPATH,'(//*[contains(text(),"₹")])[1]').get_attribute('innerText') 
    proPrice = proPrice.replace('₹','Rs')
    proPrice = proPrice.replace(',','')
    
    print(proPrice)

    for img in range(1,len(imgs)):
        try:
            imgxpath = f'//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/ul/li[{img}]/div/div/img'
            filpDriver.find_element(By.XPATH,imgxpath).click()
            
            imgloc = '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/img'
            imgloc = filpDriver.find_element(By.XPATH,imgloc).get_attribute('src')
            print(imgloc)
            # imglog = filpDriver.find_element(By.XPATH,'//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/img[1]').screenshot_as_png()
            location = 'C:/FlipkartImg/'
            with open (f'{location}{PCode}_{img}_{proPrice}.png','wb') as f:
                f.write(requests.get(imgloc).content)
        except Exception as e:
            print(e)
    return proPrice
    



Options = webdriver.ChromeOptions()
Options.add_argument("start-maximized")
filpDriver = webdriver.Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver", chrome_options=Options)
elemxpath = '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/ul/li'




if __name__ == '__main__':
     pdXlxallRec = readExcel()
     for iCount,row in pdXlxallRec.iterrows():
        print(iCount)
        if row['ToExecute'] =='Yes':
                
            PCode = row['ProductCode']
            try:
                Price = ImagDw(PCode)
                Price= Price.replace('Rs','')
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'ToExecute'] = 'No'
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'Price'] = Price

                
            except Exception as  e:
                print(e)
                pdXlxallRec.to_excel('C:/Users/Vishal/Downloads/fsn 8-6-23 upload.xlsx',sheet_name='Sheet1',index=False)
                continue


pdXlxallRec.to_excel('C:/Users/Vishal/Downloads/fsn 8-6-23 upload.xlsx',sheet_name='Sheet1',index=False)
print('Done')




