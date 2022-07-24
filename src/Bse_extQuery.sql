/*

select * from tbl_ScriptList where ToExecute='Yes' and islocked='No'

select  * from tbl_ScriptList where Script_Name like'Boro%'

update tbl_ScriptList set islocked ='Yes' 
update tbl_ScriptList set  ToExecute='Yes' where Script_Name='INFY'

select * from tbl_Bse_Results where  Script_Name like'SSWL%'

*/

-- begin tran T1
select *  from tbl_Bse_Results where Script_name in (
select Script_name from tbl_Bse_Results where Q1='Mar-22')
select * from tbl_ScriptList where ToExecute='Yes' and IsLocked='No' order by script_name 

select count(*) from tbl_ScriptList where IsLocked='Yes' and ToExecute ='Yes'
select * from tbl_ScriptList where ToExecute='Yes' and IsLocked='No'order by script_name 
select * from tbl_Bse_Results order by script_name 

select  distinct Script_name from tbl_Bse_Results where Q1 ='Mar-22'
order by script_name 

select count(*) from Nifty_Ticker


select distinct script_name from tbl_Bse_Results where Q1='01-Mar-22'order by Script_name

select * from tbl_ShareHolderScriptList where ISIN like '%|%'

-- delete from tbl_Bse_Results where Script_name in (select distinct script_name from tbl_Bse_Results where Q1='01-Mar-22')
UPDATE tbl_ShareHolderScriptList set ISIN='INE947Q01028' where ISIN = 'INE947Q01010'
 
select * from tbl_ShareHolderScriptList where ToExecute='Yes' and IsLocked='No' order by Script_Name
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
update tbl_Bse_Results set Q1=REPLACE(Q1,'Mar-22','01-Mar-22'), Q2=replace(Q2,'Dec-21','01-Dec-21'),Q3= REPLACE(Q3,'Sep-21','01-Sep-21'),Q4=REPLACE(Q4,'Jun-21','01-Jun-21'),Q5 = replace(Q5,'Mar-21','01-Mar-21')
 
update tbl_Bse_Results set Q1 = replace(Q1,'--','0'),Q2=replace(Q2,'--','0') ,Q3= REPLACE(Q3,'--','0'),
Q4=REPLACE(Q4,'--','0'), Q5=REPLACE(Q5,'--','0')

update tbl_Bse_Results set Q1= replace(Q1,',',''),Q2=replace(Q2,',','') ,Q3= REPLACE(Q3,',',''),
Q4=REPLACE(Q4,',',''), Q5=REPLACE(Q5,',','')

commit

select * from tbl_Bse_Results order by script_name

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
select *,'Mar-21' from tbl_Bse_Results
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

--  select * from tbl_ScriptList where script_name like '%ET%'

--  delete from tbl_ScriptList where Script_Name in ('KSBPUMPS','KPIT'
--  )
 

-- select * from tbl_ScriptList where isin in (
-- select Tisi from (
--  select ISIN Tisi,COUNT(*) cnt from tbl_ScriptList
--  group by ISIN
--  having count(*)>1
-- ) as T1
-- )order by 2

select * from tbl_AnnualBse_Results


select * from tbl_Bse_Results where Script_name in (select distinct script_name from tbl_Bse_Results where Q1='Dec-21')



select count(*) from tbl_ShareHolderScriptList where IsLocked='Yes' and ToExecute ='Yes'
select * from tbl_ShareHolderScriptList where IsLocked='No'order by script_name 
select * from tbl_Bse_Results order by script_name 
select  distinct Script_name from tbl_Bse_Results where Q1<>'Dec-21'
order by script_name 

select * from tbl_ShareHolding_BSE where [Quarter]='2022-03-01'

--update tbl_Bse_Results set IsLocked='Yes'

update tbl_ShareHolderScriptList set ISIN ='INE186H01022' where ISIN = 'INE412U01025'

select * from tbl_ShareHolderScriptList where ToExecute='Yes'

select * from tbl_ShareHolding_BSE

select * from tbl_ShareHolder_Temp tsp
where HoldingPerCent in (select max(HoldingPerCent)from tbl_ShareHolder_Temp tsp1 where tsp1.Script_name=tsp.Script_name 
and tsp.HolderName=tsp1.HolderName)
and [Quarter] = '2021-12-01'
and tsp.HolderName like '%JHUNJHUN%'
order by tsp.Script_name



-- update tbl_ShareHolderScriptList set ToExecute='Yes',IsLocked='No'
-- where Script_Name not in (
-- select distinct Script_name from tbl_ShareHolding_BSE  where [Quarter] = '2021-12-01'
-- )

-- update tbl_ShareHolderScriptList set IsLocked='Yes'
-

select * from tbl_annualScriptList

update tbl_ShareHolderScriptList set IsLocked='Yes'
select * from tbl_ShareHolderScriptList where Script_Name ='MARGOFIN'
select distinct Script_name from tbl_AnnualBse_Results where Q1='2022'

select [Script_Name],round(SpotPrice,-1)SpotPrice,chg,[DateTime],IndHigh,IndLow,day([dateTime])[Day],convert(time,[DateTime]) TimeOnly,CONVERT(date,[DateTime]) DateOnly  from Nifty_Ticker where [DateTime] in (
select distinct top 200 ([DateTime]) from Bse_Results.dbo.Nifty_Ticker order by [DateTime] desc
) and Script_Name <> 'INDIA VIX'

union ALL
select [Script_Name],SpotPrice,chg,[DateTime],IndHigh,IndLow,day([dateTime])[Day],convert(time,[DateTime]) TimeOnly,CONVERT(date,[DateTime]) DateOnly  from Nifty_Ticker where [DateTime] in (
select distinct top 200 ([DateTime]) from Bse_Results.dbo.Nifty_Ticker order by [DateTime] desc
) and Script_Name = 'INDIA VIX'



select top 750 round(SpotPrice,-1)SpotPrice,chg,[DateTime],IndHigh,IndLow,day([dateTime])[Day],convert(time,[DateTime]) TimeOnly,CONVERT(date,[DateTime]) DateOnly from Nifty_Ticker where Script_Name='NIFTY 50'

union all
select top 750 SpotPrice,chg,[DateTime],IndHigh,IndLow,day([dateTime])[Day],convert(time,[DateTime]) TimeOnly,CONVERT(date,[DateTime]) DateOnly from Nifty_Ticker where Script_Name='INDIA VIX'
order by [DateTime] desc


select * from tbl_AnnualBse_Results

update tbl_AnnualBse_Results set Q1 = replace(Q1,'--','0'),Q2=replace(Q2,'--','0') ,Q3= REPLACE(Q3,'--','0'),
Q4=REPLACE(Q4,'--','0'), Q5=REPLACE(Q5,'--','0')

update tbl_AnnualBse_Results set Q1= replace(Q1,',',''),Q2=replace(Q2,',','') ,Q3= REPLACE(Q3,',',''),
Q4=REPLACE(Q4,',',''), Q5=REPLACE(Q5,',','')



select top 625 round(SpotPrice,-1)SpotPrice,chg,[DateTime],IndHigh,IndLow,day([dateTime])[Day],convert(time,[DateTime]) TimeOnly,CONVERT(date,[DateTime]) DateOnly,datePart(HOUR,[DateTime]) Hrs from Nifty_Ticker where Script_Name='NIFTY 50'
order by [DateTime] desc