# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date:2019/3/27
#version: 0.9


#SUSE 11 SP3


import os
import time
import configparser

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")


systemType = cf.get("system","system_type")
tmpPath = cf.get("db","tmpPath")


class system:
    @staticmethod
    def install_gcc():
        check = 1
        if 'Centos' in systemType or 'Redhat'in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("yum install -y gcc gcc-c++")
        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("zypper install -y gcc gcc-c++")

        if 0 != check:
            print("请检查zypp源 or yum源 是否正常使用")
            os._exit(3)

    @staticmethod
    def createUserGroup():
        os.system("groupadd -g 901 db2iadm1")
        os.system("groupadd -g 902 db2fadm1")
        os.system("groupadd -g 903 dasadm1")
        os.system("useradd -g db2iadm1 -u 801 -d /home/db2inst1 -m  db2inst1")
        os.system("useradd -g db2fadm1 -u 802 -d /home/db2fenc1 -m  db2fenc1")
        os.system("useradd -g dasadm1 -u 803 -d /home/dasadm1 -m  dasusr1")
        #os.system("mkdir /db2data/ /db2log /db2arch")
        print("请设置数据库密码需要输入两次相同的:")
        os.system("passwd db2inst1")

    @staticmethod
    def tardb2():
        tarFilePath = cf.get("db","tarFilePath")
        if not os.path.exists(tarFilePath):
            print("configure file db tarFilePath not exist...................")
            os._exit(2)
        checkTardb2 = os.system("tar zxvf " + tarFilePath + " -C " + tmpPath)
        if 0 != checkTardb2:
            print("请检查此文件为tar.gz压缩包!.................................................")
            os._exit(3)
        

class db2config:

    @staticmethod
    def db2Install():
        os.system(tmpPath+"/server/db2_install")
        os.system("/opt/ibm/db2/V9.7/instance/dascrt -u dasusr1")
        os.system("/opt/ibm/db2/V9.7/instance/db2icrt -a server -u db2fenc1 db2inst1")
        os.system('su - db2inst1 -c "db2set DB2COMM=TCPIP"')
        os.system('su - db2inst1 -c "db2 update dbm cfg using SVCENAME 50000"')
        os.system('su - db2inst1 -c "db2start"')
        os.system('/opt/ibm/db2/V9.7/instance/db2iauto -on db2inst1')

def integeration():
    system.zypper()
    system.createUserGroup()
    system.tardb2()

    db2config.db2Configure()

if __name__ == '__main__':
    integeration()