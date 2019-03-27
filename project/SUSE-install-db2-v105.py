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

class system:
    @staticmethod
    #libaio Centos
    def zypper():
        checkzypper = os.system("zypper install -y gcc gcc-c++ kernel-source pam-32bit glibc-locale-32bit libstdc-32bit")
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
        print("请设置数据库密码需要输入两次相同的:")
        os.system("passwd db2inst1")

    @staticmethod
    def tardb2():
        defaultPath ="/opt/cash/software/"
        db2FileName ="v10.5fp10_linuxx64_server_t.tar.gz"
        db2tarPath = defaultPath + db2FileName

        if not os.path.exists(db2tarPath):
            db2tarPath = raw_input("默认路径不存在，请手动输入db2tar.gz文件绝对路径:...............")+db2FileName
            if not os.path.exists(db2tarPath):
                print("请输入正确路径!!!!!!!!!")
                os._exit(2)
        checkTardb2 = os.system("tar zxvf " + db2tarPath + " -C /opt")
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