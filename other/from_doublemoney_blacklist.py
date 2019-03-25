#coding=utf-8
import datetime
import csv
import cx_Oracle


#只需要更改下面对应参数
#数据库用户
dbName = 'poka'
#数据库密码
dbPasswd = '123456'
#数据库ip、端口号、数据库名
dbIp = '192.168.0.173:1521/orcl'
#生成文件名称名
#得到昨天日期并转换成字符串
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

yesterdayStr = getYesterday().strftime('%Y.%m.%d')
csv_name = yesterdayStr+ ".csv"
#生成文件存放路径
pathFile = 'D:/csv/' + csv_name
#创建数据库连接
db=cx_Oracle.connect(dbName,dbPasswd,dbIp)
#查询sql语句
sql = 'SELECT percode,coltime,mon,monver,monval,agencyno,trueflag FROM doubtmoneydata where coltime >=trunc(sysdate-1) and coltime<trunc(sysdate)'

#参数校准
printHeader = True


#代码系列
outputFile = open(pathFile,'wb')
output = csv.writer(outputFile,dialect='excel')

curs = db.cursor()
curs.execute(sql)






if printHeader:
    cols = []

for col in curs.description:
    cols.append(col[0])

print
output.writerow(cols)

for row_data in curs:
    output.writerow(row_data)

outputFile.close()
curs.close()
db.close()
print "success!"