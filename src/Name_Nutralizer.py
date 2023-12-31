
import numpy
from MSSQL_Operation import DB_Operation


class NameNutralizer:   
    
    def closeConnection():
        objDb.closeConnection()

    def getHolderName():
        get_Holder="select HolderName from NameNutralizer  where ToExecute='Yes' and IsLocked='No' order by HolderName"
        ArryScrLst = objDb.db_selectFetchone(get_Holder)
        return ArryScrLst

    def getAllHolderName():
        get_AllHolderName="select HolderName from NameNutralizer  where ToExecute='Yes' and IsLocked='No' order by HolderName"
        ArryAllHolder = objDb.db_selectFetchAll(get_AllHolderName)
        return ArryAllHolder

    def updateRecord(strHolderName):
        sqlUpdateHolder = "update NameNutralizer set ToExecute='Yes',IsLocked='Yes' where HolderName='{}'".format(strHolderName)
        # objDb =DB_Operation()
        objDb.sql_InsertUpdateAndCommit(sqlUpdateHolder)

    def unLockRecord():
        sqlUnlockRecord = "update NameNutralizer set IsLocked='No' where ToExecute='Yes'"
        # objDB = DB_Operation()
        objDb.Update_data(sqlUnlockRecord)
        objDb.sqlCommit()
    
    def updateTrnx(sqlQuery):
        # objDb=DB_Operation()
        objDb.Update_data(sqlQuery)

    def removeSpecialChar(HolderName):
        strChar=['(',')','-','\\','/','.',"&"]
        for iSplChar in strChar:
            HolderName= str(HolderName).replace(iSplChar,'')
        
        return HolderName.strip()

    def NameRating(HolderName):
        HolderName = NameNutralizer.removeSpecialChar(HolderName)
        
        iNameLen= len(str(HolderName))
        iRating=0
        for iSplitName in range(0,iNameLen-1):
            iRating = ord(HolderName[iSplitName])+iRating

        return iRating
    def strLength(strName):
        return len(strName)


    def strMatch(sWord,strHolderName): 
        if str(strHolderName).find(sWord)>=0:
            return 1
        else:
            return 0

objDb = DB_Operation()
nn = NameNutralizer
nn.unLockRecord()
lstAllHolderName = list(nn.getAllHolderName())

while True:    
    arrHolderName = nn.getHolderName()
    if (arrHolderName is None):
        nn.closeConnection()
        exit()
    nn.updateRecord(arrHolderName[0])
    strOriShareHolder = arrHolderName[0]
    strHolderName = nn.removeSpecialChar(arrHolderName[0])
    arrHolderName = strHolderName.split(" ")
        
    if (strHolderName is None):
        nn.closeConnection()
        exit()
    
    # strHolderName =str(arrHolderName)
    for lstHolder in lstAllHolderName:
        iMatch =0
        strOriName = lstHolder[0]
        lstHolder = nn.removeSpecialChar(lstHolder[0])
        arrNameSplit = lstHolder.split(" ")
        iNameLen = sum(map(nn.strLength,arrNameSplit))
        
        # lstHolder =str(lstHolder).strip()
        # iActualHolderlen = len(lstHolder)
        iActualHolderlen = iNameLen
        iExpHolderlen = len(strHolderName)
        iExpHolderlen = sum(map(nn.strLength,arrHolderName))
                    
        for i in range(0,len(arrNameSplit)):
            arrWords = strHolderName.split(" ")
            for sWord in arrNameSplit:
                # print(sWord)                                
                for sLetter in range(0,len(sWord)):
                    if strHolderName.find(sWord[:sLetter+1])>=0:
                        # iCount= sum(map(nn.strMatch,sWord[:sLetter+1],str(strHolderName)))
                        iMatch = iMatch + 1
                    else:
                        break
            if iNameLen>= iExpHolderlen:
                if iNameLen<=iMatch:
                    iMatchPercent = (iMatch/iNameLen)*100
                else:
                    iMatchPercent = (iMatch/iNameLen)*100
            else:
                if iNameLen>=iMatch:
                    iMatchPercent = (iMatch/iExpHolderlen)*100
                else:
                    iMatchPercent = (iMatch/iNameLen)*100
                    # print("Match Percentage {}\n".format(iMatchPercent))
            break
        
        # lstAllHolderName.pop(0)
        if iMatchPercent>=100:
            print("\n{} Vs {}   \nMatchPercent {}%".format(strHolderName,lstHolder,iMatchPercent))
            print("{}  \t {}".format(strOriShareHolder,strOriName))
            sql_MatchName = "Insert into NameMatch(ShareHolderName, MatchName, MatchPercent) values ('{}','{}','{}')".format(strOriShareHolder,strOriName,iMatchPercent)
            objDb.sql_InsertUpdateAndCommit(sql_MatchName)
            # iMatchPercent=0
            # break


        elif iMatchPercent>=65:
            print("*"*46)
            print("\n{} Vs \n{}   MatchPercent {}%".format(strHolderName,lstHolder,iMatchPercent))
            print("*"*46)
            print("{}  \t {}".format(strOriShareHolder,strOriName))
            sql_MatchName = "Insert into NameMatch(ShareHolderName, MatchName, MatchPercent) values ('{}','{}','{}')".format(strOriShareHolder,strOriName,iMatchPercent)
            objDb.sql_InsertUpdateAndCommit(sql_MatchName)
            
            # break
        elif  iMatchPercent >= 25:
            print("\n{} Vs {}   \nMatchPercent {}%".format(strHolderName,lstHolder,iMatchPercent))
            print("{}  \t {}".format(strOriShareHolder,strOriName))
            # iMatchPercent=0
            # brea
        else:
            sql_MatchName = "Insert into NameMatch(ShareHolderName, MatchName, MatchPercent) values ('{}','{}','{}')".format(strOriShareHolder,strOriName,iMatchPercent)
            # objDb.sql_InsertUpdateAndCommit(sql_MatchName)
        iMatchPercent=0


    
    # iNameRating = nn.NameRating(strHolderName)
    # sqlUpdateRating = "update NameNutralizer set Rating='{}' where HolderName='{}'".format(iNameRating,strHolderName)
    # nn.updateTrnx(sqlUpdateRating)
    
    sqlToExecute = "update NameNutralizer set ToExecute='No' where HolderName='{}'".format(strHolderName)
    nn.updateTrnx(sqlToExecute)
    lstAllHolderName.pop(0)

    # print(strHolderName,iNameRating)


