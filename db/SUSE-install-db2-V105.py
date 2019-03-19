# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 06-12-2018
#version: 0.0.2


#SUSE 11 SP3


import os

class system:
    def zypper(self):
        checkzypper = os.system("zypper install gcc gcc-c++ kernel-source pam-32bit glibc-locale-32bit")
        if 0!= checkzypper:
            print("请检查zypper源...........................................................")
            os._exit(1)

    def createUserGroup(self):
        os.system("groupadd -g 901 db2iadm1")
        os.system("groupadd -g 902 db2fadm1")
        os.system("groupadd -g 903 dasadm1")
        os.system("useradd -g db2iadm1 -u 801 -d /home/db2inst1 -m  db2inst1")
        os.system("useradd -g db2fadm1 -u 802 -d /home/db2fenc1 -m  db2fenc1")
        os.system("useradd -g dasadm1 -u 803 -d /home/dasadm1 -m  dasusr1")
        print("请设置数据库密码:")
        os.system("passwd db2inst1")

    def tardb2(self):
        db2FileName ="v10.5fp10_linuxx64_server_t.tar.gz"
        defaultPath ="/opt/"
        db2tarPath = defaultPath + db2FileName

        if not os.path.exists(db2tarPath):
            db2tarPath = raw_input("默认路径不存在，请手动输入db2tar.gz文件绝对路径...............")
            if not os.path.exists(db2tarPath):
                print("请输入正确路径!!!!!!!!!")
                os._exit(2)
        checkTardb2 = os.system("tar zxvf " + db2tarPath + " -C /opt")
        if 0 != checkTardb2:
            print("请检查此文件为tar.gz压缩包!.............................................")
            os._exit(3)
        os.system("/opt/server_t/db2_install")

class db2config:
    def db2Configure(self):
        os.system("")

