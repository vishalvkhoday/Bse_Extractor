'''
Created on Oct 27, 2019

@author: DELL
'''
import allure
import allure_pytest
import pytest
from DB_Operation import DB_Operation
from selenium.webdriver.common.action_chains import ActionChains
from Selenium_GridHub import *    # uncomment when executed on remote
# import Selenium_GridHub 
import time

browChrome = Driver
Driver.get("https://www.bseindia.com/")



def getScriptName():
    get_script="select * from tbl_ShareHolderScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name"
    objDb =DB_Operation(get_script)
    ArryScrLst = objDb.db_select()
    return ArryScrLst

def Navigate_PublicHolding():
    arrWin =browChrome.window_handles
    if len(arrWin)>1:
        # browChrome.switch_to_window(arrWin[1])
        browChrome.switch_to.window(arrWin[1])
        browChrome.find_element_by_xpath('//*[@id="deribody"]/div[2]/div[1]/div[3]/ul/li[2]/a').click()
        time.sleep(1)
        browChrome.close()
    else:
        browChrome.find_element_by_xpath('//*[@id="deribody"]/div[2]/div[1]/div[3]/ul/li[2]/a').click()
        
    arrWin =browChrome.window_handles
    # browChrome.switch_to_window(arrWin[1])
    if len(arrWin)>1 :
        browChrome.switch_to.window(arrWin[1])
    

def NavigateShareHoldingPage(ScriptName,INIE):
    try:
        WinHandlers()
        INIE = str(INIE).strip()
        Bse_sctTxt = browChrome.find_element_by_xpath('//*[@id="getquotesearch"]')                
        Bse_sctTxt.send_keys(INIE)
        time.sleep(3)
        try:
            if browChrome.find_element_by_xpath("//*[@id='ulSearchQuote']/li").is_displayed():
                browChrome.find_element_by_xpath("//*[@id='ulSearchQuote']/li").click()
            else:
                Bse_sctTxt.send_keys(Keys.ENTER)
        except Exception as e:
            print(e)            
            time.sleep(1)
        browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').clear()
        scr_info =None
        # scr_info =browChrome.find_element_by_xpath('//*[@id="getquoteheader"]/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]').get_attribute('innerText')
        scr_info =browChrome.find_element_by_xpath('//div[@class="ng-binding"]').get_attribute('innerText')
                                                    
        scr_info = scr_info.replace("(","")
        scr_info = scr_info.replace(")","")
        scr_info = str(scr_info).strip()
        if str(scr_info).find(INIE)==-1:
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').click()
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').send_keys(ScriptName +" ")
            time.sleep(3)
            try:
                if browChrome.find_element_by_xpath("//*[@id='ulSearchQuote']/li").is_displayed():
                    browChrome.find_element_by_xpath("//*[@id='ulSearchQuote']/li").click()
                else:
                    Bse_sctTxt.send_keys(Keys.ENTER)
            except Exception as e:
                print(e)   
            
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').clear()
            time.sleep(2) 
            scr_info =None
            scr_info =browChrome.find_element_by_xpath('//div[@class="ng-binding"]').get_attribute('innerText')
            scr_info = scr_info.replace("(","")
            scr_info = scr_info.replace(")","")

        
        if str(scr_info).find(INIE)==-1:
            print("Actual script {} Expected {} |{}".format(scr_info,ScriptName,INIE))
            return False
        else:
            try:
                # browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/thead/tr[3]').location_once_scrolled_into_view
                # browChrome.find_element_by_xpath('(//a[contains(@href,"shareholding-pattern")])[1]').click
                # browChrome.find_element(By.XPATH,'(//a[contains(@href,"shareholding-pattern")])[1]').is_displayed()
                browChrome.find_element(By.XPATH,'(//a[contains(@href,"shareholding-pattern")])[1]').click()
                # tblHeader =browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/thead/tr[3]').get_attribute('innerText')
                # if len(str(tblHeader).strip())==0:
                #     tblHeader =browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/tbody[1]').get_attribute('innerText')
            except Exception as e:
                print("Error while process {}".format(e))
                
                
         
        # try:
        #     browChrome.find_element_by_xpath('(//*[@id="tabshp"])[1]').click()
        #     time.sleep(2)
                                               
        #     browChrome.find_element_by_xpath('//*[@id="shp"]/div/div[1]/div/table/tbody/tr[16]/td/a').click()
        # except Exception as e:
        #     # browChrome.find_element_by_xpath('//*[@id="shp"]/div/div[1]/div/table/tbody/tr[16]/td/a/i').click()
        #     print("error while clicking on {}".format(e))
        #     pass
                                              
        return True
    except Exception as e:
        print('unable to navigate to results page error {}'.format(e))
        try:
            browChrome.find_element_by_xpath("//a[@href='/index.html']").click()
        except:
            browChrome.find_element_by_xpath("(//a[@href='/index.html'])[2]").click()
            
        return False


def GetTableRecord(Script,INIE):
    try:
        Navigate_PublicHolding()
        # browChrome.find_element_by_xpath('//*[@id="deribody"]/div[2]/div[1]/div[3]/ul/li[2]/a').location_once_scrolled_into_view
        t_Tbl_details = browChrome.find_element_by_xpath('//*[@id="tdData"]/table/tbody/tr[3]/td/table/tbody').get_attribute('innerText')
        t_Tbl_rowCnt = browChrome.find_element_by_xpath('//*[@id="tdData"]/table/tbody/tr[3]/td/table/tbody').get_attribute('childElementCount')
        qrtEnding = browChrome.find_element_by_xpath('//*[@id="tdData"]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]').get_attribute('innerText')
        qrtEnding = qrtEnding.replace('Quarter ending : ','')
        qrtEnding = qrtEnding.replace(' ','/')
        if len(qrtEnding)!=9:
            qrtEnding = '01/'+str(qrtEnding)
        conn = DB_Operation().db_ConnectionObject()
        try:
            
            for ii  in range(7,int(t_Tbl_rowCnt)):
                rowXpath = '//*[@id="tdData"]/table/tbody/tr[3]/td/table/tbody/tr[{}]'.format(ii)
                t_Tbl_details = browChrome.find_element_by_xpath(rowXpath).get_attribute('innerText')
                t_Tbl_details =t_Tbl_details.replace(',', '')
                t_Tbl_details =t_Tbl_details.replace("'","")
                arrTblRow = t_Tbl_details.split("\t")
                if len(arrTblRow) ==1:
                    pass
                elif len(arrTblRow)==8:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','','',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    print(len(arrTblRow))
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==9:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],'0','0',arrTblRow[8],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    print(len(arrTblRow))
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==10:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],arrTblRow[8],arrTblRow[9],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    print(len(arrTblRow))
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==11:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[7],arrTblRow[8],arrTblRow[9],arrTblRow[10],qrtEnding,INIE)
                    print(sql_insert_bseResults)
                    print(len(arrTblRow))
                    DB_Operation().Insert_data(conn,sql_insert_bseResults)
                elif len(arrTblRow)==12:
                    sql_insert_bseResults = "insert into tbl_ShareHolding_BSE values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',convert(date,'{}'),'{}')".format(Script,(arrTblRow[0])[0:99],arrTblRow[1],arrTblRow[2],arrTblRow[3],arrTblRow[4],arrTblRow[5],arrTblRow[6],arrTblRow[9],arrTblRow[10],arrTblRow[11],qrtEnding,INIE)
                    print(sql_insert_bseResults) 
                    print(len(arrTblRow))                         
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
        browChrome.switch_to_window(arrWin[0])
        browChrome.close()
        browChrome.switch_to_window(arrWin[1])


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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    getScriptName()


       
        
#             elm_res_bt = browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table')
#             time.sleep(1)
#             ActionChains(browChrome).move_to_element(elm_res_bt).click(elm_res_bt).perform()
#             ActionChains(browChrome).key_down(Keys.TAB).perform()
#             ActionChains(browChrome).key_down(Keys.ENTER).perform()