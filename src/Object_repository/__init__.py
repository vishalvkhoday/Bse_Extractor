from selenium.webdriver.common.keys import Keys
from selenium import webdriver


option =webdriver.ChromeOptions()
option.add_argument("start-maximized")
option.add_argument("disable-infobars")
option.add_argument("headless")
driver = webdriver.Chrome(chrome_options=option,executable_path='C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/chromedriver', service_args=["--verbose", "--log-path=C:/Users/DELL/git/Selenium_NSE_Algo/Additonal_Utility/Script.log","w+"])
#driver = webdriver.Ie('c:/Python36/chromedriver_242')
 

xpath_scr_txt = '//*[@id="getquotesearch"]'
xpath_res_bt = '//*[@id="res"]/div/div[1]/table/tbody'
xpath_href_lk = '//*[@id="res"]/div/div[1]/table/tbody[7]/tr/td[2]/a'
xpath_res_tbl = '//*[@id="qtly"]/table/tbody/tr/td/table[1]'
# xpath_res_tbl = '//*[@id="divmain"]/div[2]/div[2]/div/div/div[2]/div'
xpath_script_id = '/html/body/div[3]/div[4]/div/div/div[2]/div/div[1]'
xpath_script_ID_INIE ='//*[@id="getquoteheader"]/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]'
# xpath_script_ID_INIE = '//*[@id="eqcommanheader"]/div[3]/div/div[1]/div[1]/div[1]/div[2]/div/div[3]'
xpath_INIE = '/html/body/div[3]/div[4]/div/div/div[2]/div/div[5]'
xpath_Ind = '/html/body/div[3]/div[3]/div/div/div[2]/div/div[6]'
xpath_Sec_code = '/html/body/div[3]/div[4]/div/div/div[2]/div/div[4]'
xpath_tblHeader = '//*[@id="res"]/div/div[1]/table/thead/tr[3]'

def LaunchBrowser(self):
    driver.get("https://www.bseindia.com")
    driver.maximize_window()
    driver.implicitly_wait(5)
    
def Teardown(self):
    driver.close()