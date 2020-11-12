'''
Created on Oct 27, 2019

@author: DELL
'''
import allure
import allure_pytest
import pytest
from DB_Operation import DB_Operation
from Selenium_GridHub import *    # uncomment when executed on remote
# import Selenium_GridHub 
import time

browChrome = Driver
Driver.get("https://www.bseindia.com/")



def getScriptName():
    get_script="select * from tbl_ScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name"
    objDb =DB_Operation(get_script)
    ArryScrLst = objDb.db_select()
    return ArryScrLst


def NavigateResultsPage(ScriptName,INIE):
    try:
        WinHandlers()
        INIE = str(INIE).strip()
        Bse_sctTxt = browChrome.find_element_by_xpath('//*[@id="getquotesearch"]')                
        Bse_sctTxt.send_keys(INIE)
        time.sleep(3)
        Bse_sctTxt.send_keys(Keys.ENTER)
        time.sleep(1)
        browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').clear()
        scr_info =None
        scr_info =browChrome.find_element_by_xpath('//*[@id="getquoteheader"]/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]').get_attribute('innerText')
        scr_info = scr_info.replace("(","")
        scr_info = scr_info.replace(")","")
        scr_info = str(scr_info).strip()

        if str(scr_info).find(INIE)==-1:
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').click()
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').send_keys(ScriptName +" ")
            time.sleep(3)
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').send_keys(Keys.ENTER)
            browChrome.find_element_by_xpath('//*[@id="getquotesearch"]').clear()
            time.sleep(2) 
        scr_info =None
        scr_info =browChrome.find_element_by_xpath('//*[@id="getquoteheader"]/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]').get_attribute('innerText')
        scr_info = scr_info.replace("(","")
        scr_info = scr_info.replace(")","")
#         temp_scrId = str(scr_info).split("|")
        
        if str(scr_info).find(INIE)==-1:
            print("Actual script {} Expected {} |{}".format(scr_info,ScriptName,INIE))
            return False
        else:
            browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/thead/tr[3]').location_once_scrolled_into_view
            tblHeader =browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/thead/tr[3]').get_attribute('innerText')
        
        if tblHeader.find('Sep-20') == -1:
            print("Sep-20 quarter results not declared")
            return False
        else:
#             browChrome.find_element_by_xpath('(//*[@id="tabres"])[1]').click()
            time.sleep(2)
#             elm_res_bt = browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table')
#             time.sleep(1)
#             ActionChains(browChrome).move_to_element(elm_res_bt).click(elm_res_bt).perform()
#             ActionChains(browChrome).key_down(Keys.TAB).perform()
#             ActionChains(browChrome).key_down(Keys.ENTER).perform()
            try:
                browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/tbody[6]/tr/td[2]/a').click()
                time.sleep(2)
            except:
                browChrome.find_element_by_xpath('//*[@id="res"]/div/div[1]/table/tbody[7]/tr/td[2]/a').click()
                                                  
            return True
    except Exception as e:
        print('unable to navigate to results page error {}'.format(e))
        return False


def GetTableRecord(Script,INIE):
    try:
        browChrome.find_element_by_xpath('//*[@id="qtly"]/table/tbody/tr/td/table[1]').location_once_scrolled_into_view
        t_Tbl_details = browChrome.find_element_by_xpath('//*[@id="qtly"]/table/tbody/tr/td/table[1]').get_attribute('innerText')
        t_Tbl_details = t_Tbl_details.replace("Income Statement", "").replace("%", "")
        if t_Tbl_details.find('Sep-20')<0:
                  
            time.sleep(2)
        spt_Tbl_details = t_Tbl_details.splitlines()
        secID=""
        sec_code = ""
        sec_ISIN = ""
        scr_info =None
        scr_info =browChrome.find_element_by_xpath('//*[@id="getquoteheader"]/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]').get_attribute('innerText')
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
        browChrome.switch_to_window(arrWin[1])
        browChrome.close()
        browChrome.switch_to_window(arrWin[0])
        


sqlTablereset ="update tbl_ScriptList set IsLocked='No' where ToExecute='Yes'"
objTblreset = DB_Operation().db_ConnectionObject()
DB_Operation().Update_data(objTblreset,sqlTablereset)
DB_Operation().sqlCommit(objTblreset)
while(True):
    WinHandlers()
    ScriptName = getScriptName()
    if ScriptName ==None:
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
