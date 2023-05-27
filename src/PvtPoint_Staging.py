
import time

from MSSQL_Operation import DB_Operation

SQL_Q = """-- select distinct trnx_date from tbl_PvtPoint_Staging order by 1 desc

insert into tbl_PvtPoint_Staging
select * from v_PivotPoint_Staging where LastVol >= Vol60Day and cls between pvtpoint and [Target]


delete from NSE_EOD_Staging where Trnx_date = (select max(Trnx_date) from NSE_EOD_Staging)

"""

conn = DB_Operation()

for i in range(0,1500):
    conn.InsertUpdate_data(SQL_Q)
    print(i)
    if i == 150 or i== 300 or i==450 or i==600:
        pass
        print('Stop here ')


    time.sleep(1)
    
