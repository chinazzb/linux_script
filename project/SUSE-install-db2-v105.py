# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 06-12-2018
#version: 0.9


#SUSE 11 SP3


import os
import configparser


cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")

class system:
    @staticmethod
    #libaio Centos
    def zypper():
        checkzypper = os.system("zypper install -y gcc gcc-c++ kernel-source pam glibc-locale libstdc")
        if 0!= checkzypper:
            print("请检查zypper源...........................................................")
            os._exit(1)

    @staticmethod
    def createUserGroup():
        #hosts = raw_input("请输入IP、主机名,格式如下\n192.168.1.2 linux-db:")
        #os.system("echo >> /etc/hosts/ " + hosts)
        os.system("groupadd -g 901 db2iadm1")
        os.system("groupadd -g 902 db2fadm1")
        os.system("groupadd -g 903 dasadm1")
        os.system("useradd -g db2iadm1 -u 801 -d /home/db2inst1 -m  db2inst1")
        os.system("useradd -g db2fadm1 -u 802 -d /home/db2fenc1 -m  db2fenc1")
        os.system("useradd -g dasadm1 -u 803 -d /home/dasadm1 -m  dasusr1")
        #os.system("mkdir /db2data/ /db2log /db2arch")
        dbPassword = cf.get("db","db_pass")
        os.system("echo " + dbPassword + " | passwd --stdin db2inst1")

    @staticmethod
    def tardb2():
        db2tarFile = cf.get("db","tarFilePath")
        #tmpPath = cf.get("db","tmpPath")

        if not os.path.exists(db2tarFile):
            print("请输入正确路径!!!!!!!!!")
            os._exit(2)
        checkTardb2 = os.system("tar zxvf " + db2tarFile + " -C /opt")
        if 0 != checkTardb2:
            print("请检查此文件为tar.gz压缩包!.................................................")
            os._exit(3)
        

class db2config:

    @staticmethod
    def db2Configure():
        os.system("/opt/server_t/db2_install")
        os.system("/opt/ibm/db2/V10.5/instance/dascrt -u dasusr1")
        os.system("/opt/ibm/db2/V10.5/instance/db2icrt -a server -u db2fenc1 db2inst1")
        os.system('su - db2inst1 -c "db2set DB2COMM=TCPIP"')
        os.system('su - db2inst1 -c "db2 update dbm cfg using SVCENAME 50000"')
        os.system('su - db2inst1 -c "db2start"')
        os.system('/opt/ibm/db2/V10.5/instance/db2iauto -on db2inst1')

def install_DB2V105():
    system.zypper()
    system.createUserGroup()
    system.tardb2()
    db2config.db2Configure()

if __name__ == '__main__':
    install_DB2V105()