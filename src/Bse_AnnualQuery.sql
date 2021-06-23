select * from tbl_AnnualBse_Results

select distinct script_name
from tbl_AnnualBse_Results

select * from tbl_AnnualScriptList where ToExecute='Yes'

select * from tbl_ScriptList where Script_Name ='SSWL'

select * from tbl_Bse_Results where Script_name = 'A2ZINFRA'


select  * from tbl_Bse_Results br  right outer join tbl_ScriptList sc ON
br.Script_Name=sc.Script_name
and br.ISIN=sc.ISIN
--and br.Script_Name <> null
and sc.ToExecute='Yes'
order by sc.Script_name

