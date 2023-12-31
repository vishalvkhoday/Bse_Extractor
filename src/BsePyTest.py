'''
Created on Oct 27, 2019

@author: DELL
'''
import allure
import allure_commons
import allure_pytest
import pytest
from DB_Operation import DB_Operation
# from Selenium_GridHub import *    # uncomment when executed on remote
# import Selenium_GridHub 
import time,selenium

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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


@allure.step("Get ScriptName")
def getScriptName():
    get_script="select * from tbl_ScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name"
    objDb =DB_Operation(get_script)
    ArryScrLst = objDb.db_select()
    return ArryScrLst

def ObjExist(Obj):
    if Obj.is_displayed():
        return True
    else:
        False



def NavigateResultsPage(ScriptName,INIE):
    try:
        WinHandlers()
        INIE = str(INIE).strip()
        Bse_sctTxt = browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]')                
        Bse_sctTxt.send_keys(INIE +" ")
        time.sleep(2)
        Bse_sctTxt.send_keys(Keys.BACK_SPACE)
        time.sleep(2)
        try:
            if browChrome.find_element(By.XPATH,"//*[@id='ulSearchQuote']/li").is_displayed():
                # browChrome.find_element(By.XPATH,"//*[@id='ulSearchQuote']/li").click()
                strSuggest_Xpath = "//*[contains(text(),'{}')]".format(INIE)
                ObjFirstSuggestion = browChrome.find_element(By.XPATH,strSuggest_Xpath)
                if ObjExist(ObjFirstSuggestion) == True:
                    browChrome.find_element(By.XPATH,strSuggest_Xpath).click()
                else:
                    Bse_sctTxt.send_keys(Keys.ENTER)
            else:
                Bse_sctTxt.send_keys(Keys.ENTER)
        except Exception as e:
            print(e)            
            time.sleep(1)
        browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').clear()
        scr_info =None
        scr_info =browChrome.find_element(By.XPATH,'//div[@class="ng-binding ng-scope"]').get_attribute('innerText')
        scr_info = scr_info.replace("(","")
        scr_info = scr_info.replace(")","")
        scr_info = str(scr_info).strip()

        if str(scr_info).find(INIE)==-1:
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').click()
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').send_keys(ScriptName +" ")
            time.sleep(3)
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').send_keys(Keys.ENTER)
            browChrome.find_element(By.XPATH,'//*[@id="getquotesearch"]').clear()
            time.sleep(2) 
            scr_info =None
            scr_info =browChrome.find_element(By.XPATH,'//div[@class="ng-binding ng-scope"]').get_attribute('innerText')
            scr_info = scr_info.replace("(","")
            scr_info = scr_info.replace(")","")
#         temp_scrId = str(scr_info).split("|")
        WebDriverWait(browChrome,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="res"]/div/div[1]/table/thead/tr[3]')))
        tblHeader =browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/thead/tr[3]').get_attribute('innerText')
        if tblHeader.find('Sep-23') == -1:
            print("Sep-23 quarter results not declared")
            return False
        else:
#             browChrome.find_element_by_xpath('(//*[@id="tabres"])[1]').click()
            time.sleep(2)
        
        if str(scr_info).find(INIE)==-1:
            print("Actual script {} Expected {} |{}".format(scr_info,ScriptName,INIE))
            return False
        else:
            time.sleep(2)
            browChrome.find_element(By.XPATH,"(//a[contains(text(),'Financials')])[2]").location_once_scrolled_into_view
            if ObjExist(browChrome.find_element(By.XPATH,"(//a[contains(@href,'results')])[1]")) == True:
                browChrome.find_element(By.XPATH,"(//a[contains(@href,'results')])[1]").click()
            else:
                
                time.sleep(1)
                browChrome.find_element(By.XPATH,"(//a[contains(text(),'Financials')])[2]").click()
                time.sleep(2)
                browChrome.find_element(By.XPATH,"(//a[contains(@href,'results')])[1]").click()
            # browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/thead/tr[3]').location_once_scrolled_into_view
            
        
        

#             try:
                
#                 # browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/tbody[6]/tr/td[2]/a').click()
#                 browChrome.find_element(By.XPATH,"(//a[contains(text(),'Financials')])[2]").click()
#                 browChrome.find_element(By.XPATH,"(//a[contains(@href,'results')])[1]").click()

#                 time.sleep(2)
#             except:
#                 try:
#                     browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/tbody[7]/tr/td[2]/a').click()
#                 except:
#                     browChrome.find_element(By.XPATH,'//*[@id="res"]/div/div[1]/table/tbody[4]/tr/td[2]/a').click()
                                                  
            return True
        
    except Exception as e:
        print('unable to navigate to results page error {}'.format(e))
        return False


def GetTableRecord(Script,INIE):
    try:
        time.sleep(2)
        browChrome.find_element(By.XPATH,'//*[@id="qtly"]/table/tbody/tr/td/table[1]').location_once_scrolled_into_view
        t_Tbl_details = browChrome.find_element(By.XPATH,'//*[@id="qtly"]/table/tbody/tr/td/table[1]').get_attribute('innerText')
        t_Tbl_details = t_Tbl_details.replace("Income Statement", "").replace("%", "")
        if t_Tbl_details.find('Sep-23')!=-1:
                             
            time.sleep(2)
            spt_Tbl_details = t_Tbl_details.splitlines()
            secID=""
            sec_code = ""
            sec_ISIN = ""
            scr_info =None
            scr_info =browChrome.find_element(By.XPATH,'//div[@class="ng-binding ng-scope"]').get_attribute('innerText')
            scr_info = scr_info.replace("(","")
            scr_info = scr_info.replace(")","")
            temp_scrId = str(scr_info).split("|")
            temp_scrId = temp_scrId
            secID = temp_scrId[0]
            sec_code =temp_scrId[1]
            sec_ISIN = temp_scrId[2]
            print(sec_code,secID)
            if str(sec_ISIN.strip()) != str(INIE).strip():
                # assert False
                return False
            else:
                pass
                conn = DB_Operation().db_ConnectionObject()
                for row in spt_Tbl_details:
                    if len(row)>0:
                        col = row.split('\t')
                        if col[1] == 'Standalone':
                            break

                        if len(col)>= 6:
                            sql_insert_bseResults = "insert into tbl_Bse_Results values('{}','{}','{}','{}','{}','{}','{}','{}')".format(Script,INIE,col[0],col[1],col[2],col[3],col[4],col[5])
                        elif len(col)== 5:
                            sql_insert_bseResults = "insert into tbl_Bse_Results values('{}','{}','{}','{}','{}','{}','{}','0')".format(Script,INIE,col[0],col[1],col[2],col[3],col[4])
                        elif len(col)== 4:
                            sql_insert_bseResults = "insert into tbl_Bse_Results values('{}','{}','{}','{}','{}','{}','0','0')".format(Script,INIE,col[0],col[1],col[2],col[3])
                        elif len(col)== 3:
                            sql_insert_bseResults = "insert into tbl_Bse_Results values('{}','{}','{}','{}','{}','0','0','0')".format(Script,INIE,col[0],col[1],col[2])
                        elif len(col)== 2:
                            sql_insert_bseResults = "insert into tbl_Bse_Results values('{}','{}','{}','{}','0','0','0','0')".format(Script,INIE,col[0],col[1])
                                            
                        
                        DB_Operation().Insert_data(conn,sql_insert_bseResults)
                    else:
                        continue
                DB_Operation().sqlCommit(conn)
                print("After insert commit performed..")
                assert True
        else:
            return False
    except:
        try:
            DB_Operation().sqlRollBack(conn)
            print("Rollback performed..")
            return False
        except:
            return False

def WinHandlers():
    arrWin =browChrome.window_handles
    if len(arrWin)>1:
        # browChrome.switch_to_window(arrWin[0])
        browChrome.switch_to.new_window('tab')
        browChrome.close()
        # browChrome.switch_to_window(arrWin[1])
        browChrome.switch_to.new_window('window')
        


sqlTablereset ="update tbl_ScriptList set IsLocked='No' where ToExecute='Yes'"
objTblreset = DB_Operation().db_ConnectionObject()
DB_Operation().Update_data(objTblreset,sqlTablereset)
DB_Operation().sqlCommit(objTblreset)
while(True):
    WinHandlers()
    ScriptName = getScriptName()
    try:
        browChrome.find_element(By.XPATH,'//*[@id="myimg"]/div/div/div/p/button').click()
    except:
        pass

    if ScriptName == None:
        print("No more script to execute")
        sqlTablereset ="update tbl_ScriptList set IsLocked='No' where ToExecute='Yes'"
        objTblreset = DB_Operation().db_ConnectionObject()
        DB_Operation().Update_data(objTblreset,sqlTablereset)
        DB_Operation().sqlCommit(objTblreset)
        break
    else:
        sql_UpdateLock = "update tbl_ScriptList set IsLocked='Yes' where Script_Name = '{}'".format(ScriptName[0])
        ObjUpdatelock = DB_Operation().db_ConnectionObject()
        DB_Operation().Update_data(ObjUpdatelock,sql_UpdateLock)
        DB_Operation().sqlCommit(ObjUpdatelock)
        PageStatus =NavigateResultsPage(ScriptName[0],ScriptName[1])
        if PageStatus ==True:
            RecordExeSts =GetTableRecord(ScriptName[0],ScriptName[1])
            if RecordExeSts == False:
                sqlExecuteFlag = "update tbl_ScriptList set ToExecute='Yes' where Script_Name = '{}'".format(ScriptName[0])
            else:
                sqlExecuteFlag = "update tbl_ScriptList set ToExecute='No' where Script_Name = '{}'".format(ScriptName[0])
            sqlUpdateEXE = DB_Operation().db_ConnectionObject()
            DB_Operation().Update_data(sqlUpdateEXE,sqlExecuteFlag)
            DB_Operation().sqlCommit(sqlUpdateEXE)
        else:
            pass
            
print("Done....")
browChrome.quit()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    getScriptName()
