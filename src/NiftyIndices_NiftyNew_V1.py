'''
Created on Sep 20, 2020

@author: DELL
'''
from datetime import datetime
from time import sleep
import json
import fnc
import random
import requests
import sys
import os

if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from DB_Operation import DB_Operation

try:
    from neon_config import build_neon_insert_values, ensure_neon_table, get_neon_connection
except ImportError:
    from neon_config import build_neon_insert_values, ensure_neon_table, get_neon_connection


def safe_string(value):
    if value is None:
        return ''
    return str(value).strip()


def should_insert_in_neon(script_name):
    allowed = {'NIFTY 50', 'INDIA VIX', 'NIFTY BANK'}
    return script_name.upper() in {name.upper() for name in allowed}


def test_Nifty():
    neon_conn = None
    local_conn = None
    try:
        neon_conn = get_neon_connection()
        if neon_conn is not None:
            neon_table_name = ensure_neon_table(neon_conn)
            print(f'Neon connection initialized. Using table: {neon_table_name}')
        else:
            neon_table_name = None
    except Exception as e:
        print(e)
        neon_conn = None
        neon_table_name = None

    try:
        local_conn = DB_Operation().db_ConnectionObject()
    except Exception as e:
        print(f"Local DB connection failed: {e}")
        local_conn = None

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
                    DtTm = jsonAllIndex["timestamp"]
                    Niftyticker = list(fnc.map(('index','last','percentChange','open','high','low','previousClose'),jsonAllIndex["data"]))

                    for x in Niftyticker:
                        try:
                            Script_Name = safe_string(x[0])
                            SpotPrice = safe_string(x[1]).replace(',', '')
                            chg = safe_string(x[2])
                            IndOpen = safe_string(x[3]).replace(',', '')
                            IndHigh = safe_string(x[4]).replace(',', '')
                            IndLow = safe_string(x[5]).replace(',', '')
                            IndPreClose = safe_string(x[6]).replace(',', '')


                            sql_insertQuery = "insert into nifty_ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) values ('{}','{}','{}','{}','{}','{}','{}','{}')".format(Script_Name, DtTm, SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose)

                            if local_conn is not None:
                                try:
                                    local_cur = local_conn.cursor()
                                    local_cur.execute(sql_insertQuery)
                                    local_conn.commit()
                                    local_cur.close()
                                    print(f"Inserted record for {Script_Name}, {DtTm},{SpotPrice} into local database.")
                                except Exception as e:
                                    # print(f"Local SQL insert failed for {Script_Name}: {e}")
                                    local_conn.rollback()

                            if should_insert_in_neon(Script_Name):
                                if neon_conn is not None and neon_table_name is not None:
                                    try:
                                        neon_record = (
                                            Script_Name,
                                            DtTm,
                                            SpotPrice,
                                            chg,
                                            IndOpen,
                                            IndHigh,
                                            IndLow,
                                            IndPreClose,
                                        )
                                        with neon_conn.cursor() as neon_cur:
                                            neon_cur.execute(
                                                f'''
                                                INSERT INTO {neon_table_name} (script_name, datetime, spotprice, chg, indopen, indhigh, indlow, indpreclose)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                                ''',
                                                build_neon_insert_values(neon_record),
                                            )
                                        neon_conn.commit()
                                    except Exception as e:
                                        # print(f"Neon insert failed for {Script_Name}: {e}")
                                        neon_conn.rollback()

                        except Exception as e:
                            print(f"Record skipped due to validation error: {e}")
                            continue

                    iRant = random.randint(90,112)
                    for i in range(iRant,-1,-1):
                        print("Next refresh in {} seconds  ".format(i), end = "\r")
                        sleep(1)
                    
            except Exception as e:
                # print(e)
                pass
                # print(f"Error fetching data: {response.status_code}")
                
    
                
        
    except Exception as e:
        print(e)

    if local_conn is not None:
        try:
            local_conn.close()
        except Exception:
            pass

    if neon_conn is not None:
        neon_conn.close()
            
if __name__ == "__main__":
    test_Nifty()
    
