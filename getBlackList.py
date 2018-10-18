# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Shenzhen Poka
#Author: Duan Yu
#Mail:  cn-duanyu@foxmail.com or chinazzbcn@gmail.com

import datetime
import csv
import cx_Oracle
import shutil

#get Yesterday date 获得昨日日期
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

#save file path 保存文件路径
def saveFilePath(filePath):
    yesterdayStr = getYesterday().strftime('%Y%m%d')
    csv_name = 'blackList' + yesterdayStr+ ".csv"
    filePath = filePath + csv_name
    return filePath

#writer file
def writerFile(dbUser,dbPasswd,dbIp,sql,filePath,backPath,logPath):
    dbConnect = cx_Oracle.connect(dbUser,dbPasswd,dbIp)
    curs = dbConnect.cursor()
    curs.execute(sql)
    printHeader = True
    ###字段名和表数据
    if printHeader:
        cols= []
    for col in curs.description:
        cols.append(col[0])

    outPutFile = open(saveFilePath(filePath),'wb+')
    outPut = csv.writer(outPutFile)
    #写入字段
    outPut.writerow(cols)
    ##写入表数据
    outPut.writerows(curs)
    ##关闭连接
    outPutFile.close()
    curs.close()
    dbConnect.close()
    ###备份和日志
    shutil.copy(saveFilePath(filePath),backPath)
    logDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logFile = open(logPath,'a+')
    logFile.write(logDate+'生成csv文件成功,存放路径在'+saveFilePath(filePath)+'\n')


if __name__ == '__main__':
    dbUser='poka'
    dbPasswd='123456'
    dbIp='9.109.79.104:1521/orcl'
    sql = 'SELECT percode,coltime,mon,monver,monval,agencyno,trueflag FROM doubtmoneydata ' \
          'where coltime >=trunc(sysdate-1) and coltime<trunc(sysdate)'
    filePath = 'D:/csv/'
    backPath = 'E:/getBlackListBack/csv//'
    logPath = 'D:/from_doublemoney_blacklist/getBlackListBack.log'
    writerFile(dbUser,dbPasswd,dbIp,sql,filePath,backPath,logPath)