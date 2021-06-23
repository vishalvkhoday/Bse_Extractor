'''
Created on Nov 20, 2020

@author: DELL
'''

from Selenium_GridHub import *
from DB_Operation import *
from time import sleep
brwChrom = Driver


def getScriptName():
    get_script="select * from tbl_ScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name"
    objDb =DB_Operation(get_script)
    ArryScrLst = objDb.db_select()
    return ArryScrLst

def getScriptDetails():
    WebDriverWait(brwChrom,30).until(EC.visibility_of_element_located((By.XPATH,"//h1[@class='pcstname']/../div[1]")),"Script details information")
    strScriptDetails = brwChrom.find_element_by_xpath("//h1[@class='pcstname']/../div[1]").get_attribute("innerText")
    strScriptDetails = strScriptDetails.replace("\n\n", "").replace("Trade\nPortfolio", "")
    arrScrDetails = strScriptDetails.split("|")
    return list(arrScrDetails)
    
    

def SearchErrorExist():
    try:
        if brwChrom.find_element_by_class_name("gD_20 MT10").is_displayed() == True:
            return True
    except:
        return False

def test_launchBrow():
    arrSrc_Name = getScriptName()
    Src_Name = arrSrc_Name[0]
    ISIN =arrSrc_Name[1]
    brwChrom.get("https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/shanthigears/SG04")
    brwChrom.find_element_by_xpath("//form[@id='form_topsearch']/input[@id='search_str']").click()
    brwChrom.find_element_by_xpath("//form[@id='form_topsearch']/input[@id='search_str']").send_keys(Src_Name)
    sleep(1)
    ActionChains(brwChrom).key_down(Keys.ENTER).perform()
    sleep(2)
    strSearchError = SearchErrorExist()
    
    if strSearchError ==True:
        brwChrom.find_element_by_xpath("//form[@id='form_topsearch']/input[@id='search_str']").click()
        brwChrom.find_element_by_xpath("//form[@id='form_topsearch']/input[@id='search_str']").send_keys(ISIN)
        sleep(1)
        ActionChains(brwChrom).key_down(Keys.ENTER).perform()
        sleep(2)
    
    lstScrdetails = getScriptDetails()
    print(lstScrdetails)
    brwChrom.find_elements_by_partial_link_text("vishal").click
test_launchBrow()