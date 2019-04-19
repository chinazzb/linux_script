# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/4/11


import os


def largecash(filePath):
    for lineList in open(filePath):
        print("####################################################################################")
        lineListSplit = str(lineList).split(",")
        oldOrgcode=lineListSplit[0]
        newOrgcode=lineListSplit[1]

        print('db2 "update THINK.BANKNOTICE set bankno = ' + newOrgcode +' where bankno = '+oldOrgcode+'"')
        print('db2 "update THINK.BULLETIN_BOARD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.COMPANY set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.EARLYWARNINGSEETIME set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.EARLYWHITELIST set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.FOCUSATTENTIONTOCOMPANY set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.FOCUSATTENTIONTOINDUSTRYCATEGORY set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.FOCUSATTENTIONTOPERSON set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "delete from THINK.ORGANIZATION where orgcode = ' +newOrgcode +'"')
        print('db2 "delete from THINK.ORGANIZATION_BUSINESS where orgcode = ' +newOrgcode +'"')
        print('db2 "delete from THINK.ORGANIZATION_EQUIPMENT where orgcode = ' +newOrgcode +'"')
        print('db2 "delete from THINK.ORGANIZATION_SEARRECORD where orgcode = ' +newOrgcode +'"')
        print('db2 "delete from THINK.ORGLATLNG where orgcode = ' +newOrgcode +'"')
        print('db2 "delete from THINK.ORGPOINTINFO where orgcode = ' +newOrgcode +'"')
        print('db2 "delete from THINK.USERS where orgcode = ' +newOrgcode +'"')

        print('db2 "update THINK.ORGANIZATION set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION set parentcode = ' +newOrgcode +' where parentcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_BUSINESS set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_EQUIPMENT set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_SEARRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_TRADE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGLATLNG set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGPOINTINFO set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PARAMTYPE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PRIVATEACCOUNTAPPOINTMENT set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')

        print('db2 "update command options using c off"')
        print('db2 "alter table think.privateaccountrecord activate not logged initially "')
        print('db2 "update THINK.PRIVATEACCOUNTRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "commit"')
        print('db2 "update command options using c on"')

        print('db2 "update THINK.PRIVATEACCOUNTUNCONFIRMEDRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PRIVATERECORDWARNINGORGCODE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PRIVATERECORDWARNINGPROBLEM set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PRIVATEWARNINGCALCUL set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PUBLICACCOUNTAPPOINTMENT set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')

        print('db2 "update command options using c off"')
        print('db2 "alter table think.PUBLICACCOUNTRECORD activate not logged initially "')
        print('db2 "update THINK.PUBLICACCOUNTRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "commit"')
        print('db2 "update command options using c on"')

        print('db2 "update THINK.PUBLICACCOUNTUNCONFIRMEDRECORD set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PUBLICRECORDWARNINGORGCODE set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PUBLICRECORDWARNINGPROBLEM set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PUBLICWARNINGCALCUL set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.TAG set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.TAG_ORGANIZATION set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.USERS set orgcode = ' +newOrgcode +' where orgcode = '+oldOrgcode+'"')
    # def evaluate():
def evaluate(filePath):
    for lineList in open(filePath):
        print("####################################################################################")
        lineListSplit = str(lineList).split(",")
        oldOrgcode=lineListSplit[0]
        newOrgcode=lineListSplit[1]

        print('db2 "update THINK.ANTICURRENCYEXCHANGE set organizationno = ' + newOrgcode +'where organizationno = '+oldOrgcode+'"')
        print('db2 "update THINK.ANTIFAKEACTIVITY set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.BANKNOTICE set bankno = ' + newOrgcode +'where bankno = '+oldOrgcode+'"')
        print('db2 "update THINK.BULLETIN_BOARD set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.CANBIEXCHANGE set organizationno = ' + newOrgcode +'where organizationno = '+oldOrgcode+'"')
        print('db2 "update THINK.COMPANY set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.COMPANY_ACCOUNT set accountorgcode = ' + newOrgcode +'where accountorgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.COUNTERFEITCAPTURE set organizationno = ' + newOrgcode +'where organizationno = '+oldOrgcode+'"')
        print('db2 "update THINK.COUPONADJUST set organizationno = ' + newOrgcode +'where organizationno = '+oldOrgcode+'"')
        print('db2 "update THINK.EARLYWHITELIST set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.EVALUATE_HISTORY set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.EVALUATE_HISTORY_GROUP set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.EVALUATIONGRADE set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "delete from THINK.ORGANIZATION where orgcode = newOrgcode"')
        print('db2 "delete from THINK.ORGANIZATION_BUSINESS where orgcode = newOrgcode"')
        print('db2 "delete from THINK.ORGANIZATION_EQUIPMENT where orgcode = newOrgcode"')
        print('db2 "delete from THINK.ORGANIZATION_SEARRECORD where orgcode = newOrgcode"')
        print('db2 "delete from THINK.ORGLATLNG where orgcode = newOrgcode"')
        print('db2 "delete from THINK.ORGPOINTINFO where orgcode = newOrgcode"')
        print('db2 "delete from THINK.USERS where orgcode = newOrgcode"')

        print('db2 "update THINK.ORGANIZATION set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION set parentcode = ' + newOrgcode +'where parentcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_BUSINESS set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_EQUIPMENT set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGANIZATION_SEARRECORD set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGLATLNG set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORGPOINTINFO set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORG_EVALUATE_SCORE set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.ORG_EVALUATE_SCORE_DETAILS set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PADEXPORTDATARECORD set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PARAMTYPE set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PLANINFO set createorgcode = ' + newOrgcode +'where createorgcode = '+oldOrgcode+'"')

        print('db2 "update command options using c off"')
        print('db2 "alter table think.PLAN_ENTITYDATEREPORTINFO activate not logged initially "')
        print('db2 "update THINK.PLAN_ENTITYDATEREPORTINFO set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "commit"')
        print('db2 "update command options using c on"')

        print('db2 "update command options using c off"')
        print('db2 "alter table think.PLAN_ENTITYINFO activate not logged initially "')
        print('db2 "update THINK.PLAN_ENTITYINFO set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "commit"')
        print('db2 "update command options using c on"')

        print('db2 "update THINK.PLAN_NOSERVERDATE set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.PLAN_ORGREPORT_ORGCODE set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_ADMINISTRATIVEPENALTY set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_CASHCOMPLAINT set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_CASHRMBCLEARSITUATION set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_CHECKCOUNTERFEITMONEY set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_ERRORRECORD set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_SORTMISTAKE set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.REPORT_SORTRANDOMCHECK set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SMALLMONRYEARLYWARNING set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SUBCASH_DETAIL set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SUBCASH_HISDETAIL set replyorgcode = ' + newOrgcode +'where replyorgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SUBCASH_REQUEST set replyorgcode = ' + newOrgcode +'where replyorgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SUBCASH_REQUEST set requesterorgcode = ' + newOrgcode +'where requesterorgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SURVEY_RECORD set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.SYS_MESSAGE set receive_orgcode = ' + newOrgcode +'where receive_orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.TAG set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.TAG_ORGANIZATION set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.TARGET_VALUEINFO set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')
        print('db2 "update THINK.USERS set orgcode = ' + newOrgcode +'where orgcode = '+oldOrgcode+'"')

if __name__ == '__main__':
    evaluate("../test/orgcode.txt")