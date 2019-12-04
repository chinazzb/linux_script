# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/10/22
#version: 0.9


#SUSE 11 SP3


import os
import configparser
import time

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")
systemType = cf.get("system","systemType")

class system:
    @staticmethod
    #libaio Centos
    def basis():
        hostName = cf.get("system","hostName")
        hostIp = cf.get("system","hostIp")
        hosts = hostIp + "    " + hostName

        os.system("echo " + hosts +" >> /etc/hosts")
        check = 0
        if 'Centos' in systemType or 'Redhat'in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("")
            os.system("echo " + hostName + " > /etc/hostname")

        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("zypper in -y gcc gcc-c++ kernel-source pam glibc-locale libstdc++-devel-32bit")
            os.system("echo " + hostName + " > /etc/HOSTNAME")
            os.system("sysctl -w kernel.hostname=" + hostName)

        if 0 != check:
            print("check zypp or yum repolist")
            os._exit(3)



    @staticmethod
    def firewalld():
        openPortList = cf.get("system","openPort")
        openPortListSplit = str(openPortList).split(" ")

        if "Centos" in systemType or "Redhat" in systemType:
            os.system("systemctl start firewalld")
            os.system("systemctl enable firewalld")
            for i in range(len(openPortListSplit)):
                os.system("firewall-cmd --permanent --zone=public --add-port="+openPortListSplit[i]+"/tcp")
            os.system("firewall-cmd --reload")

        elif "SUSE" in systemType:
            firewallFile ="/etc/sysconfig/SuSEfirewall2"
            replace(firewallFile,'FW_SERVICES_EXT_TCP=""','FW_SERVICES_EXT_TCP="'+openPortList+'"')
            os.system("rcSuSEfirewall2 start")
            os.system("chkconfig SuSEfirewall2_init on")
            os.system("chkconfig SuSEfirewall2_setup on")
        

class db2:


    @staticmethod
    def createUserGroup():
        print("starting create user group..........................................")

        check = 0
        os.system("groupadd -g 901 db2iadm1")
        os.system("groupadd -g 902 db2fadm1")
        os.system("groupadd -g 903 dasadm1")
        os.system("useradd -g db2iadm1 -u 801 -d /home/db2inst1 -m  db2inst1")
        os.system("useradd -g db2fadm1 -u 802 -d /home/db2fenc1 -m  db2fenc1")
        os.system("useradd -g dasadm1 -u 803 -d /home/dasadm1 -m  dasusr1")
        #dbPassword = cf.get("db2","dbPass")
        #check += os.system("echo " + dbPassword + " | passwd --stdin db2inst1")

        if 0 != check:
            print("create user group db2 failure.................................")
            os._exit(10)

        print("done create user group..........................................")


    @staticmethod
    def tardb2():
        print("starting unpacking db2 .....................................")

        tarFilePath = cf.get("db2","tarFilePath")
        if not os.path.exists(tarFilePath):
            print("")
            os._exit(2)
        checkTardb2 = os.system("tar zxvf " + tarFilePath + " -C /opt > /dev/null 2>&1")
        if 0 != checkTardb2:
            print("unpacking db2 failure...................................................")
            os._exit(11)

        print("done unpacking db2 ....................................")

    @staticmethod
    def db2Install():
        print("staring db2 fome")

        dbPort = cf.get("db2","dbPort")
        check = os.system("/opt/server_t/db2_install -b /opt/ibm/db2/V10.5 -p SERVER")
        check += os.system("/opt/ibm/db2/V10.5/instance/dascrt -u dasusr1")
        check += os.system("/opt/ibm/db2/V10.5/instance/db2icrt -a server -u db2fenc1 db2inst1")
        check += os.system('su - db2inst1 -c "db2set DB2COMM=TCPIP"')
        check += os.system('su - db2inst1 -c "db2 update dbm cfg using SVCENAME ' + dbPort + '"')
        check += os.system('su - db2inst1 -c "db2start"')
        check += os.system('/opt/ibm/db2/V10.5/instance/db2iauto -on db2inst1')

        if 0 != check:
            print("db2 install failure............................................")
            os._exit(12)

def replace(file_path, old_str, new_str):
    try:
        f = open(file_path,'r+')
        all_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_lines:
            line = line.replace(old_str, new_str)
            f.write(line)
        f.close()
    except Exception,e:
        print e

def integeration():
    system.basis()
    system.firewalld()

    db2.createUserGroup()
    db2.tardb2()
    db2.db2Install()

if __name__ == '__main__':
    integeration()