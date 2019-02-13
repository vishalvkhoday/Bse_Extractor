'''
Created on Feb 9, 2019

@author: vkhoday
'''


import  os
import  time
import Object_repository as Obj_R
from selenium.common.exceptions import ErrorInResponseException as EIR 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from Object_repository import driver
import Bse_Extractor_V1 as Bse
import win32ctypes
import re



driver = Obj_R.driver


for i in range(1,5):
    try:
        os.system("python C:/Users/vkhoday/eclipse-workspace/Bse_Results_extractor/src/Bse_Extractor_V1.py")        
        tempath = os.system('del /q/f/s %TEMP%\*')
#         print (tempath)
        win_hand =driver.window_handles
        print ('{}'.format(win_hand))
        for win in win_hand:
            driver.switch_to.window(win)
            driver.quit()
        
        time.sleep(120)
        print('{}time\'s to be executed'.format(i))
    except:
        time.sleep(120)
        continue

    