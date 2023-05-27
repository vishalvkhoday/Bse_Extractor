
from datetime import datetime
import datetime
import time

from MSSQL_Operation import DB_Operation

SQL_Get_TrdDate = """
select cast(trnx_date as date) from tbl_Trnx_date where
trnx_date between '2007-01-01'and '2019-12-31'
order by 1
"""



conn = DB_Operation()

getTrdDate = conn.db_selectFetchAll(SQL_Get_TrdDate )


for tdate in getTrdDate:
    rowList =tdate[0]
    SQL_Insert_Returnz =  """     insert into [dbo].[tbl_ReturnzOnEq_V1]     exec [dbo].[sp_Returnz_On_Equity] @@Trnx = '{}-{}-{}'""".format(rowList.year,rowList.month,rowList.day)
    conn.InsertUpdate_data(SQL_Insert_Returnz)
    print (SQL_Insert_Returnz)
    