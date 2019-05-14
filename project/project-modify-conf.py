# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 07-12-2018
#version: 0.9-p

import os
import configparser
import time

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")
databaseType = cf.get("project","databaseType")

def modifyDatabaseConfFile():
    print("modify project db.properties")

    installPath = cf.get("project","installPath")
    hostIp = cf.get("system","hostIp")
    dbUser = cf.get(databaseType,"dbUser")
    dbPort = cf.get(databaseType,"dbPort")
    dbPass = cf.get(databaseType,"dbPass")
    dbName = cf.get(databaseType,"dbName")
    projectType = cf.get("project","projectType")

    dbConfigPath = installPath + projectType + "/WEB-INF/classes/db.properties"

    #DB_TYPE
    dbType = "DB_TYPE=" + databaseType
    checkType = os.system("sed -i '1c " + dbType + " ' " + dbConfigPath)

    #DB_URL
    DB_URL= "DB_URL=" + hostIp + ":" + dbPort
    checkURL = os.system("sed -i '2c " + DB_URL + " ' " + dbConfigPath)

    #DB_NAME
    dbName = "DB_NAME=" + dbName
    checkName = os.system("sed -i '3c " + dbName + " ' " + dbConfigPath)

    #DB_USERNAME
    dbUser = "DB_USER=" + dbUser
    checkUser = os.system("sed -i '4c " + dbUser + " ' " + dbConfigPath)

    #DB_PASSWORD
    dbPass = "DB_PASSWORD=" + dbPass
    checkPass = os.system("sed -i '5c " + dbPass + " ' " + dbConfigPath)

    print("done project db.properties")

def modifyConfFile():

if __name__ == '__main__':
    modifyDatabaseConfFile()