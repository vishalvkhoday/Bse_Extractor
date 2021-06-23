/*

select count(*) from tbl_Bse_Results
select * from tbl_ScriptList where ToExecute='No' and islocked='No'

select  * from tbl_ScriptList where Script_Name like'Boro%'

update tbl_ScriptList set islocked ='Yes' 
update tbl_ScriptList set  ToExecute='Yes' where Script_Name='INFY'


select * from tbl_ScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name

select * from tbl_Bse_Results where  Script_Name like'SSWL%'

*/

-- begin tran T1
-- DELETE from tbl_Bse_Results where Script_name in (
-- select Script_name from tbl_Bse_Results where Q1='01-Mar-21')


select count(*) from tbl_ScriptList where IsLocked='Yes' and ToExecute ='Yes'
select * from tbl_ScriptList where IsLocked='No'order by script_name 
select * from tbl_Bse_Results order by script_name 
select  distinct Script_name from tbl_Bse_Results order by script_name 

-- select * from tbl_Bse_Results where Q1='Mar-21' order by script_name
-- select max(trnx_date) from nse_eod
-- select distinct [quarter] from Bse_Results order by 1

--select * from tbl_ScriptList where script_name like '%INFY%'
--select * from Nifty_Ticker where Script_Name='Nifty 50' order by [datetime]  desc


--select * from tbl_scriptList where script_name like'KTK%'

/*
select * from tbl_ScriptList where ISIN in (
select ISIN from (
select  ISIN,count(*) cnt from tbl_scriptList
group by ISIN
having count(*) >1
) as t1
) */
/*


select * from tbl_Bse_Results

rollback
Begin Tran T1
update tbl_Bse_Results set Q1=REPLACE(Q1,'Mar-21','01-Mar-21'),Q2=REPLACE(Q2,'Dec-20','01-Dec-20'),Q3 = replace(Q3,'Sep-20','01-Sep-20'),
Q4=replace(Q4,'Jun-20','01-Jun-20') ,Q5= REPLACE(Q5,'Mar-20','01-Mar-20')
 
update tbl_Bse_Results set Q1 = replace(Q1,'--','0'),Q2=replace(Q2,'--','0') ,Q3= REPLACE(Q3,'--','0'),
Q4=REPLACE(Q4,'--','0'), Q5=REPLACE(Q5,'--','0')

update tbl_Bse_Results set Q1= replace(Q1,',',''),Q2=replace(Q2,',','') ,Q3= REPLACE(Q3,',',''),
Q4=REPLACE(Q4,',',''), Q5=REPLACE(Q5,',','')

commit

select * from tbl_Bse_Results

Begin Tran T2
update Temp_Bse_Results set ISIN = s.ISIN from Temp_Bse_Results br inner join Sector s on
br.Script_Name=s.Script_Name

update Temp_Bse_Results set Sector= s.Sector from Temp_Bse_Results br inner join Sector s on
br.Script_Name=s.Script_Name

update Bse_Results set NPM = tbr.NPM from Bse_Results br inner join Temp_Bse_Results tbr on
br.Script_Name=tbr.Script_Name
and br.[Quarter]=tbr.[Quarter]
and br.NPM <> tbr.NPM


insert into Bse_Results
select * from Temp_Bse_Results
except
select * from Bse_Results
order by Script_Name


select * from Bse_Results where Script_Name in (
select scr from (
select Script_Name scr,[Quarter]qtr,count(*) cnt from Bse_Results
group by Script_Name,[Quarter]
having count(*) >1
)as T1
) order by Script_Name,[Quarter]

commit
rollback
*/

/*

select * from DailyHotPick where LastVol> Vol60Day and 
LastVol>AvgVol
and  Trnx_date =(select  max(Trnx_date) from DailyHotPick)

*/

/*

insert into tbl_Bse_Results_Archive
select *,'SMarep-21' from tbl_Bse_Results
except
select * from tbl_Bse_Results_Archive


truncate table tbl_Bse_Results
commit
*/
/*
 select * from nse_eod where trnx_date in (
 select max(Trnx_date) from nse_eod)
 order by script_name
 */