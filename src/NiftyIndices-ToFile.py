'''
Created on Sep 20, 2020

@author: DELL
'''
from datetime import datetime
from DB_Operation import DB_Operation
from time import sleep
import json
import fnc
import os
import random
import requests
    
def test_Nifty():    
    try:
        while True:
            
            now = datetime.now()
            mkthh =now.strftime('%H%M')
            if (int(mkthh) >= 1535):
                print("Market is closed, exiting script.")
                # break

            url = "https://www.nseindia.com/api/allIndices"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.nseindia.com/"
            }
            try:                          
                    
                # Session for cookies
                session = requests.Session()
                session.headers.update(headers)
                try:
                    response = session.get(url)
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}\n Error fetching data:")
                    sleep(5)  # Wait before retrying
                    continue
                if response.status_code != 200:
                    print(f"Error fetching data: {response.status_code}")
                    sleep(5)  # Wait before retrying
                    continue
                strJson = response.text
                jsonAllIndex = json.loads(strJson)
                DtTm = str(jsonAllIndex["timestamp"]).replace(' ','_').replace(':','_')

                output_dir = r"C:\\Test\\"
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"{DtTm}.json")
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(strJson)

                print(f"Timestamp: {DtTm}")
                print(f"Saved response to: {output_file}")
                
            
                
                iRant = random.randint(96,116)
                for i in range(iRant,-1,-1):
                    print("Next refresh in {} seconds  ".format(i), end = "\r")
                    sleep(1)
                    
            except Exception as e:
                print(e)
                # print(f"Error fetching data: {response.status_code}")
                
    
                
        
    except Exception as e:
        print(e)          
            
if __name__ == "__main__":
    test_Nifty()
    
