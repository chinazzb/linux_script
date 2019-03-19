# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 07-12-2018
#version: 0.9

def writeFile():
    parameterArr =()
    while True:
        print("如下格式db2,127.0.0.1,50000,cash,db2inst1,Cash123+")
        parameter = raw_input("请输入数据库连接参数,参考上面格式使用“,”分隔:")
        parameterArr = parameter.split(',')
        if len(parameterArr) == 6:
            break

    defaultConfFilePath = "/usr/local/tomcat/webapps/largecash/WEB-INF/classes/"
    defaultConfFileName = "db.properties"
    confFile = open('C:\\Users\\DuanYU\\Desktop\\temp\\test.txt','w')
    if 'mysql' == parameterArr[0]:
        confFile.write("SQL_DRIVER=com.mysql.jdbc.Driver\n")
        confFile.write("SQL_URL=jdbc\:mysql\://"+parameterArr[1]+"\:"+parameterArr[2]+"/"+parameterArr[3]+
                       "?useUnicode\=true&characterEncoding\=UTF-8&allowMultiQueries\=true\n")
        confFile.write("SQL_USERNAME="+parameterArr[4]+"\n")
        confFile.write("SQL_PASSWORD="+parameterArr[5]+"\n")
        confFile.close()
    elif 'db2' == parameterArr[0]:
        confFile.write("SQL_DRIVER=com.ibm.db2.jcc.DB2Driver\n")
        confFile.write("SQL_URL=jdbc:db2://"+parameterArr[1]+":"+parameterArr[2]+"/"+parameterArr[3]+"\n")
        confFile.write("SQL_USERNAME="+parameterArr[4]+"\n")
        confFile.write("SQL_PASSWORD="+parameterArr[5]+"\n")
        confFile.close()

if __name__ == '__main__':
    writeFile()