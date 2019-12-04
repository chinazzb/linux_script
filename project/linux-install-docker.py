# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization:Poka China
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/10/22


import configparser
import os
import time

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath, encoding="utf-8-sig")

systemType = cf.get("system","systemType")
systemd = cf.get("system","systemd")

installPath = cf.get("docker","installPath")



class system:

    @staticmethod
    def basis():
        hostName = cf.get("system","hostName")
        check = 0
        if 'Centos' in systemType or 'Redhat'in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("yum install -y gcc gcc-c++ bash-completion > /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/hostname")

        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("zypper install -y gcc gcc-c++ bash-completion > /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/HOSTNAME")

        if 0 != check:
            print("请检查zypp源 or yum源 是否正常使用")
            os._exit(3)

    @staticmethod
    def firewall():
        time.sleep(3)
        print("configuring system firewalld.......................")

        openPortList = cf.get("system","openPort")
        openPortListSplit = str(openPortList).split(" ")
        #Centos Redhat
        if 'Centos' in systemType or 'Redhat' in systemType:
            os.system("systemctl start firewalld")
            os.system("systemctl enable firewalld")
            for i in range(len(openPortListSplit)):
                os.system("firewall-cmd --permanent --zone=public "
                          "--add-port="+openPortListSplit[i] + "/tcp >/dev/null 2>&1")
            os.system("firewall-cmd --reload")
        elif 'SUSE' in systemType:
            firewallFile ="/etc/sysconfig/SuSEfirewall2"
            replace(firewallFile,'FW_SERVICES_EXT_TCP=""','FW_SERVICES_EXT_TCP="'+openPortList+'"')
            os.system("rcSuSEfirewall2 start")
            os.system("chkconfig SuSEfirewall2_init on")
            os.system("chkconfig SuSEfirewall2_setup on")

        print("done configure system firewalld")

class docker:

    @staticmethod
    def tarFile():
        print("staring tarFile docekr ..........................................")

        tarFilePath = cf.get("docker","tarFilePath")
        tmpPath = cf.get("docker","tmpPath")
        check = os.system("tar zxvf " + tarFilePath + " -C " + tmpPath + " > /dev/null 2>&1")
        check += os.system("mv " + tmpPath + "/docker/* " + installPath)

        if 0 != check:
            print("tarFile docker failure.............................................")
            os._exit(11)

        print("done tarFile docker ...............................................")

    @staticmethod
    def group():
        print("staring create group user ......................")

        check = os.system("groupadd docker && useradd -g docker docker")

        if 0 != check:
            print("create group user failure..............................")
            os._exit(12)

        print("done create group user ............................")

    @staticmethod
    def swarmCluster():
        print("test.....")


    @staticmethod
    def init():
        print("staring init.d docekr.................................................")

        check = os.system("cp ./conf/docker/* /usr/lib/systemd/system/")
        check += os.system("systemctl enable docker")

        if 0 != check:
            print("init.d docker failure........................................")

        print("done init.d docker ...................................................")

    @staticmethod
    def format():
        print("staring docker........................................")

        check = os.system("systemctl start docker")
        check += os.system("cp ./conf/docker/daemon.json /etc/docker/")
        check += os.system("cp ./conf/docker/docker /usr/share/bash-completion/completions/ ")
        check += os.system("systemctl restart docker")
        if 0 != check:
            print("staring docker failure .......................................")
            os._exit(14)

        print("done start docker ...........................................")
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
    system.firewall()

    docker.tarFile()
    docker.group()
    docker.swarmCluster()
    docker.init()
    docker.format()

if __name__ == '__main__':
    integeration()