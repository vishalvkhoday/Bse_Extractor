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


select *,DATEPART(Q,[Quarter]) from tbl_ShareHolding_BSE where DATEPART(Q,[Quarter]) =2
and YEAR([Quarter])='2022'
order by Script_name

select distinct [quarter] from tbl_ShareHolding_BSE
order by 1


select * from tbl_ShareHolderScriptList where ToExecute='No'
update tbl_ShareHolderScriptList set ToExecute='Yes',IsLocked='No'