
import numpy
from MSSQL_Operation import DB_Operation


class NameNutralizer:   
    
    def closeConnection():
        objDb.closeConnection()

    def getHolderName():
        get_Holder="select * from NameNutralizer  where ToExecute='Yes' and IsLocked='No' order by HolderName"
        
        ArryScrLst = objDb.db_selectFetchone(get_Holder)
        return ArryScrLst
       
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

    

    def NameRating(HolderName):
        strChar=['(',')','-','\\','/']
        for iSplChar in strChar:
            HolderName= str(HolderName).replace(iSplChar,'')

        
        iNameLen= len(str(HolderName))
        iRating=0
        for iSplitName in range(0,iNameLen-1):
            iRating = ord(HolderName[iSplitName])+iRating

        return iRating

objDb =DB_Operation()
nn=NameNutralizer
nn.unLockRecord()

while True:    
    arrHolderName = nn.getHolderName()
    if str(arrHolderName)=='None':
        nn.closeConnection()
        exit()
        
    strHolderName =arrHolderName[0]
    nn.updateRecord(strHolderName)
    iNameRating = nn.NameRating(strHolderName)
    sqlUpdateRating = "update NameNutralizer set Rating='{}' where HolderName='{}'".format(iNameRating,strHolderName)
    nn.updateTrnx(sqlUpdateRating)
    sqlToExecute = "update NameNutralizer set ToExecute='No' where HolderName='{}'".format(strHolderName)
    nn.updateTrnx(sqlToExecute)

    print(strHolderName,iNameRating)


