from  selenium import webdriver
import pytest
import selenium.webdriver.common.by
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
import requests

# Change file path here 
def readExcel():
    xlSheet = pd.read_excel('C:/Vishal/git/Bse_Extractor/src/AmazonProductList.xlsx',sheet_name='Sheet1')
    xlPd =pd.DataFrame(data=xlSheet)
    # xlPd = xlPd.loc[xlPd['ToExecute'] == 'Yes']

    
    return xlPd


def ImagDw(PCode):
    filpDriver.get(f"https://www.amazon.in//dp/{PCode}")
    filpDriver.maximize_window()
    imgs = filpDriver.find_elements(By.XPATH,elemxpath)
    try:
        proPrice = filpDriver.find_element(By.XPATH,'(//*[contains(text(),"M.R.P")])/../../../../div[1]/span[2]/span[1]').get_attribute('innerText') 
        proPrice = proPrice.replace('₹','Rs')
        proPrice = proPrice.replace(',','')
        MRP = filpDriver.find_element(By.XPATH,'(//*[contains(text(),"M.R.P")])[1]').get_attribute('innerText')
    except:
        proPrice = 0
        MRP = 0
        
        pass
    ProdDesc = filpDriver.find_element(By.XPATH,'//span[@id="productTitle"]').get_attribute('innerText')
    
    print(proPrice)
    location = 'c:/Amazon/'

    for img in range(3,len(imgs)):
        try:
            imgxpath = f'//*[@id="altImages"]/ul/li[{img}]'
            filpDriver.find_element(By.XPATH,imgxpath).click()
            
        
            imgloc = '//div[@class="imgTagWrapper"]/img'
            # imgloc = filpDriver.find_element(By.XPATH,imgloc).get_attribute('src')
            imglocs = filpDriver.find_elements(By.XPATH,imgloc)
            for imgs in imglocs:
                imgloc =imgs.get_attribute('src')
                print(imgloc)
                with open (f'{location}{PCode}_{img}.png','wb') as f:
                    f.write(requests.get(imgloc).content)
            
                        
        except Exception as e:
            print(e)
    return proPrice,MRP,ProdDesc
    

Options = webdriver.ChromeOptions()
Options.add_argument("--start-maximized")

# service = Service(executable_path="D:/flipkart/chromedriver.exe")
service = Service(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver")

filpDriver = webdriver.Chrome(service=service)

elemxpath = '//*[@id="altImages"]/ul/li'

if __name__ == '__main__':
     pdXlxallRec = readExcel()
     for iCount,row in pdXlxallRec.iterrows():
        print(iCount)
        if row['ToExecute'] =='Yes':
                
            PCode = row['ProductCode']
            try:
                retVal = ImagDw(PCode)
                Price = str(retVal[0])
                Price= Price.replace('Rs','')
                MRP_Val = retVal[1]
                ProdDes = retVal[2]
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'ToExecute'] = 'No'
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'Price'] = Price
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'MRP'] = MRP_Val
                pdXlxallRec.loc[pdXlxallRec['ProductCode']== PCode,'ProductDesc'] = ProdDes

                
            except Exception as  e:
                print(e)
                pdXlxallRec.to_excel('C:/Vishal/git/Bse_Extractor/src/AmazonProductList.xlsx',sheet_name='Sheet1',index=False)
                continue


pdXlxallRec.to_excel('C:/Vishal/git/Bse_Extractor/src/AmazonProductList.xlsx',sheet_name='Sheet1',index=False)
print('Done')
