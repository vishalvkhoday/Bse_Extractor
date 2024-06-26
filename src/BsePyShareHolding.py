'''
Created on Oct 27, 2019

@author: DELL
'''
import allure
import allure_pytest
import pytest
from DB_Operation import DB_Operation
from selenium.webdriver.common.action_chains import ActionChains
# from Selenium_GridHub import *    # uncomment when executed on remote
# import Selenium_GridHub 
import time
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


Options = ChromeOptions()
Options.add_argument("start-maximized")
# Options.add_argument("headless")
Options.add_argument("disable-infobar")
serviceObj = Service('C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver.exe')


browChrome =  webdriver.Chrome(service=serviceObj,options=Options) #Driver
# browChrome = webdriver.Chrome(executable_path="C:/Vishal/git/Bse_Extractor/src/WebDriver/chromedriver", chrome_options=Options) #Driver
browChrome.get("https://www.bseindia.com/")


# browChrome = Driver
# Driver.get("https://www.bseindia.com/")

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)
# logger = logging.getLogger(__name__)

def getScriptName():
    get_script="select * from tbl_ShareHolderScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name"
    objDb =DB_Operation(get_script)
    ArryScrLst = objDb.db_select()
    return ArryScrLst

def Navigate_PublicHolding():
    time.sleep(2)
    arrWin =browChrome.window_handles
    
    if len(arrWin)>1:
        # browChrome.switch_to_window(arrWin[1])
        browChrome.switch_to.window(arrWin[1])
        browChrome.execute_script("window.scrollTo(50,775)")
        time.sleep(1)
        browChrome.find_element(By.XPATH,'//*[@id="deribody"]/div[2]/div[1]/div[3]/ul/li[2]/a').click()
        
        browChrome.close()
    else:
        browChrome.execute_script("window.scrollTo(50,775)")
        time.sleep(1)
        # browChrome.find_element(By.XPATH,'//*[@id="deribody"]/div[2]/div[1]/div[3]/ul/li[2]/a').click()
        browChrome.find_element(By.XPATH,"//a[contains(text(),'the Public shareholder')]").click()
        time.sleep(1)
        
    arrWin =browChrome.window_handles
    # browChrome.switch_to_window(arrWin[1])
    if len(arrWin)>1 :
        browChrome.switch_to.window(arrWin[1])
    

def NavigateShareHoldingPage(ScriptName,INIE):
    try:
        WinHandlers()
        INIE = str(INIE).strip()
        Bse_sctTxt = browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]')                
        Bse_sctTxt.send_keys(INIE+ " ")
        time.sleep(1)
        Bse_sctTxt.send_keys(Keys.BACK_SPACE)
        time.sleep(2)
        try:
            if browChrome.find_element(By.XPATH,"//*[@id='ulSearchQuote']/li").is_displayed():
                # browChrome.find_element(By.XPATH,"//*[@id='ulSearchQuote']/li").click()
                try:
                    temp_Script = str(ScriptName).lower()
                    listXpath = "//a[contains(@href,'{}')]".format(temp_Script)
                    browChrome.find_element(By.XPATH,listXpath).click()
                except Exception as e:
                    Bse_sctTxt.send_keys(Keys.ENTER)

            else:
                Bse_sctTxt.send_keys(Keys.ENTER)
        except Exception as e:
            print(e)            
            time.sleep(1)
        browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').clear()
        scr_info =None
        # scr_info =browChrome.find_element(By.XPATH,'//*[@id="getquoteheader"]/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]').get_attribute('innerText')
        scr_info =browChrome.find_element(By.XPATH,'//*[@class="home_widget"]/div[2]').get_attribute('innerText')
        
        # browChrome.find_element(By.XPATH,'//*[@id="divmain"]/footer/div/div/div/div[1]/a[4]').location_once_scrolled_into_view
        
        scr_info = scr_info.replace("(","")
        scr_info = scr_info.replace(")","")
        scr_info = str(scr_info).strip()
        aryScript = scr_info.split("|")
        if str(ScriptName).strip() ==str(aryScript[0]).strip():
            print (ScriptName,INIE)
        else:
            print (ScriptName,INIE," Actual ",aryScript[0])
            
            

        if str(scr_info).find(INIE)==-1:
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').click()
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').send_keys(ScriptName +" ")
            time.sleep(1)
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').send_keys(Keys.BACK_SPACE)
            try:
                if browChrome.find_element(By.XPATH,"//*[@id='ulSearchQuote']/li").is_displayed():
                    browChrome.find_element(By.XPATH,"//*[@id='ulSearchQuote']/li").click()
                else:
                    Bse_sctTxt.send_keys(Keys.ENTER)
            except Exception as e:
                print(e)   
            
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').clear()
            time.sleep(2) 
            scr_info =None
            scr_info =browChrome.find_element(By.XPATH,'//div[@class="ng-binding"]').get_attribute('innerText')
            scr_info = scr_info.replace("(","")
            scr_info = scr_info.replace(")","")

        
        if str(scr_info).find(INIE)==-1:
            print("Actual script {} Expected {} |{}".format(scr_info,ScriptName,INIE))
            return False
        else:
            try:
                # browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/thead/tr[3]').location_once_scrolled_into_view
                time.sleep(1)
                browChrome.execute_script("window.scrollTo(50,775)")
                browChrome.find_element(By.XPATH,'//*[@class="panel-title"]/a[contains(@href,"shareholding-pattern")]').click()
                # oResult =browChrome.find_element(By.XPATH,'//*[@id="tabshp"]')
                # oResult.click()
                # browChrome.find_element(By.XPATH,'(//a[@id="tabshp"])[1]').click()
                # browChrome.find_element(By.XPATH,'(//i[@class="fa fa-arrow-circle-right"])[3]').click()
                # browChrome.find_element(By.XPATH,"//a[contains(@href,'shareholding-pattern')]").click()
                # tblHeader =browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/thead/tr[3]').get_attribute('innerText')
                # if len(str(tblHeader).strip())==0:
                #     tblHeader =browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/tbody[1]').get_attribute('innerText')
            except Exception as e:
                browChrome.find_element(By.XPATH,'//*[@id="shp"]/div/div[1]/div/table/tbody/tr[16]/td/a/i').location_once_scrolled_into_view
                browChrome.find_element(By.XPATH,'(//a[@id="tabshp"])[1]').click()                 
                browChrome.find_element(By.XPATH,"(//i[@class='fa fa-arrow-circle-right'])[3]").click()
                browChrome.find_element(By.XPATH,"(//i[@class='fa fa-arrow-circle-right'])[3]").click()
                
                print("Error while process {}".format(e))
                
                
         
        # try:
        #     browChrome.find_element(By.XPATH,'(//*[@id="tabshp"])[1]').click()
        #     time.sleep(2)
                                               
        #     browChrome.find_element(By.XPATH,'//*[@id="shp"]/div/div[1]/div/table/tbody/tr[16]/td/a').click()
        # except Exception as e:
        #     # browChrome.find_element(By.XPATH,'//*[@id="shp"]/div/div[1]/div/table/tbody/tr[16]/td/a/i').click()
        #     print("error while clicking on {}".format(e))
        #     pass
                                              
        return True
    except Exception as e:
        print('unable to navigate to results page error {}'.format(e))
        try:
            browChrome.find_element(By.XPATH,"//a[@href='/index.html']").click()
        except:
            try:
                browChrome.find_element(By.XPATH,"(//a[@href='/index.html'])[2]").click()
            except Exception as e :
                print(e)
            
        return False


def GetTableRecord(Script,INIE):
    try:
        time.sleep(1)
        Navigate_PublicHolding()
        # browChrome.find_element(By.XPATH,'//*[@id="deribody"]/div[2]/div[1]/div[3]/ul/li[2]/a').location_once_scrolled_into_view
        t_Tbl_details = browChrome.find_element(By.XPATH,'//*[@id="tdData"]/table/tbody/tr[3]/td/table/tbody').get_attribute('innerText')
        t_Tbl_rowCnt = browChrome.find_element(By.XPATH,'//*[@id="tdData"]/table/tbody/tr[3]/td/table/tbody').get_attribute('childElementCount')
        qrtEnding = browChrome.find_element(By.XPATH,'//*[@id="tdData"]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]').get_attribute('innerText')
        qrtEnding = qrtEnding.replace('Quarter ending : ','')
        qrtEnding = qrtEnding.replace(' ','/')
        if qrtEnding == '31-Mar-23':
            pass
        elif len(qrtEnding)!=9 or qrtEnding=='March/2023':
            qrtEnding = '01/'+str(qrtEnding)
        conn = DB_Operation().db_ConnectionObject()
        try:
            
            for ii  in range(7,int(t_Tbl_rowCnt)):
                rowXpath = '//*[@id="tdData"]/table/tbody/tr[3]/td/table/tbody/tr[{}]'.format(ii)
                t_Tbl_details = browChrome.find_element(By.XPATH,rowXpath).get_attribute('innerText')
                t_Tbl_details =t_Tbl_details.replace(',', '')
                t_Tbl_details =t_Tbl_details.replace("'","").replace("-",'')
                arrTblRow = t_Tbl_details.split("\t")
                if len(arrTblRow) ==1:
                    pass
                elif len(arrTblRow)==8:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','','',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==9:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],'0','0',arrTblRow[8],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==10:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],arrTblRow[8],arrTblRow[9],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==11:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','0','0','0',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==12:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],'','',arrTblRow[8],qrtEnding,INIE)
                    print(sql_insert_bseResults) 
                                           
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==13:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],'',arrTblRow[8],arrTblRow[9],qrtEnding,INIE)
                    print(sql_insert_bseResults) 
                                           
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                
                elif len(arrTblRow)==15:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],'',arrTblRow[10],arrTblRow[11],qrtEnding,INIE)
                    print(sql_insert_bseResults) 
                                           
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                    

                else :
                    return False
                    break
                
            arrWin =browChrome.window_handles
            browChrome.switch_to.window(arrWin[1])
            browChrome.close()
            browChrome.switch_to.window(arrWin[0])
            DB_Operation().sqlCommit(conn)
            assert True    
        except Exception as e:
            print(e)
            DB_Operation().sqlRollBack(conn)
            arrWin =browChrome.window_handles
            # browChrome.switch_to_window(arrWin[1])
            browChrome.switch_to.window(arrWin[1])
            browChrome.close()
            # browChrome.switch_to_window(arrWin[0])
            browChrome.switch_to.window(arrWin[0])
            return False
                   
            
        
    except Exception as e:
        try:
            print("Error orrcured {}".format(e))
            DB_Operation().sqlRollBack(conn)
            print("Rollback performed..")
            return False
        except:
            return False

def WinHandlers():
    arrWin =browChrome.window_handles
    if len(arrWin)>1:
        # browChrome.switch_to_window(arrWin[0])
        browChrome.switch_to.window(arrWin[0])
        browChrome.close()
        browChrome.switch_to.window(arrWin[1])


sqlTablereset ="update tbl_ShareHolderScriptList set IsLocked='No' where ToExecute='Yes'"
objTblreset = DB_Operation().db_ConnectionObject()
DB_Operation().Update_data(objTblreset,sqlTablereset)
DB_Operation().sqlCommit(objTblreset)
while(True):
    WinHandlers()
    ScriptName = getScriptName()
    if ScriptName ==None:
        print("No more script to execute")
        sqlTablereset ="update tbl_ShareHolderScriptList set IsLocked='No' where ToExecute='Yes'"
        objTblreset = DB_Operation().db_ConnectionObject()
        DB_Operation().Update_data(objTblreset,sqlTablereset)
        DB_Operation().sqlCommit(objTblreset)
        break
    else:
        sql_UpdateLock = "update tbl_ShareHolderScriptList set IsLocked='Yes' where Script_Name = '{}'".format(ScriptName[0])
        ObjUpdatelock = DB_Operation().db_ConnectionObject()
        DB_Operation().Update_data(ObjUpdatelock,sql_UpdateLock)
        DB_Operation().sqlCommit(ObjUpdatelock)
        PageStatus =NavigateShareHoldingPage(ScriptName[0],ScriptName[1])
    if PageStatus ==True:
            RecordExeSts =GetTableRecord(ScriptName[0],ScriptName[1])
            if RecordExeSts == False:
                sqlExecuteFlag = "update tbl_ShareHolderScriptList set ToExecute='Yes' where Script_Name = '{}'".format(ScriptName[0])
            else:
                sqlExecuteFlag = "update tbl_ShareHolderScriptList set ToExecute='No' where Script_Name = '{}'".format(ScriptName[0])
            sqlUpdateEXE = DB_Operation().db_ConnectionObject()
            DB_Operation().Update_data(sqlUpdateEXE,sqlExecuteFlag)
            DB_Operation().sqlCommit(sqlUpdateEXE)
            arrWin =browChrome.window_handles
            if len(arrWin)>1:
                browChrome.close()        
                # browChrome.switch_to_window(arrWin[0])
                browChrome.switch_to.window(arrWin[0])
            else:
                pass
    else:
        pass
            
print("Done....")
browChrome.quit()


# if __name__ == "__main__":
#     # import sys;sys.argv = ['', 'Test.testName']
#     getScriptName()


       
        
#             elm_res_bt = browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table')
#             time.sleep(1)
#             ActionChains(browChrome).move_to_element(elm_res_bt).click(elm_res_bt).perform()
#             ActionChains(browChrome).key_down(Keys.TAB).perform()
#             ActionChains(browChrome).key_down(Keys.ENTER).perform()