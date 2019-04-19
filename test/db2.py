# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/4/11


import os


def getOrgcode(filePath):
    for lineList in open(filePath):
        lineListSplit = str(lineList).split(",")
        oldOrgcode=lineListSplit[0]
        newOrgcode=lineListSplit[1]

def largecash(newOrgcode,oldOrgcode):
    os.system('db2 "update THINK.BANKNOTICE set bankno = ' + newOrgcode +' where bankno = '+oldOrgcode+'"')
    os.system('db2 "update THINK.BULLETIN_BOARD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.COMPANY set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.EARLYWARNINGSEETIME set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.EARLYWHITELIST set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.FOCUSATTENTIONTOCOMPANY set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.FOCUSATTENTIONTOINDUSTRYCATEGORY set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.FOCUSATTENTIONTOPERSON set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "delete from THINK.ORGANIZATION where orgcode = ' +newOrgcode +'"')
    os.system('db2 "delete from THINK.ORGANIZATION_BUSINESS where orgcode = ' +newOrgcode +'"')
    os.system('db2 "delete from THINK.ORGANIZATION_EQUIPMENT where orgcode = ' +newOrgcode +'"')
    os.system('db2 "delete from THINK.ORGANIZATION_SEARRECORD where orgcode = ' +newOrgcode +'"')
    os.system('db2 "delete from THINK.ORGLATLNG where orgcode = ' +newOrgcode +'"')
    os.system('db2 "delete from THINK.ORGPOINTINFO where orgcode = ' +newOrgcode +'"')
    os.system('db2 "delete from THINK.USERS where orgcode = ' +newOrgcode +'"')

    os.system('db2 "update THINK.ORGANIZATION set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGANIZATION set parentcode = ' +newOrgcode +' where parentcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGANIZATION_BUSINESS set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGANIZATION_EQUIPMENT set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGANIZATION_SEARRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGANIZATION_TRADE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGLATLNG set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.ORGPOINTINFO set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PARAMTYPE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PRIVATEACCOUNTAPPOINTMENT set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')

    os.system('db2 "update command options using c off"')
    os.system('db2 "alter table think.privateaccountrecord activate not logged initially "')
    os.system('db2 "update THINK.PRIVATEACCOUNTRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "commit"')
    os.system('db2 "update command options using c on"')

    os.system('db2 "update THINK.PRIVATEACCOUNTUNCONFIRMEDRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PRIVATERECORDWARNINGORGCODE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PRIVATERECORDWARNINGPROBLEM set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PRIVATEWARNINGCALCUL set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PUBLICACCOUNTAPPOINTMENT set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 ""')
    os.system('db2 ""')
    os.system('db2 "update command options using c off"')
    os.system('db2 "alter table think.PUBLICACCOUNTRECORD activate not logged initially "')
    os.system('db2 "update THINK.PUBLICACCOUNTRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "commit"')
    os.system('db2 "update command options using c on"')

    os.system('db2 "update THINK.PUBLICACCOUNTUNCONFIRMEDRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PUBLICRECORDWARNINGORGCODE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PUBLICRECORDWARNINGPROBLEM set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.PUBLICWARNINGCALCUL set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.TAG set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.TAG_ORGANIZATION set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    os.system('db2 "update THINK.USERS set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')

def cashflow():

if __name__ == '__main__':
    getOrgcode("./orgcode.txt")