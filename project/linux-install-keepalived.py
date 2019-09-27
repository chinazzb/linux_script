# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/9/23


import configparser
import os
import time

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath, encoding="utf-8-sig")

systemType = cf.get("system","systemType")
systemd = cf.get("system","systemd")

tmpPath = cf.get("keepalived","tmpPath")

class system:

    @staticmethod
    def basis():
        hostName = cf.get("system","hostName")
        check = 1
        if 'Centos' in systemType or 'Redhat'in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("yum install -y gcc gcc-c++ openssl-devel libnl libnl-devel libnfnetlink-devel net-tools > /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/hostname")

        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("zypper install -y  gcc gcc-c++ openssl libopenssl-devel > /dev/null 2>&1")
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
            os.system("sed -i '894s/^#FW/FW/g' " + firewallFile)
            os.system("sed -i '895s/^/#/g' " + firewallFile)
            os.system("rcSuSEfirewall2 start")
            os.system("chkconfig SuSEfirewall2_init on")
            os.system("chkconfig SuSEfirewall2_setup on")

        print("done configure system firewalld")


class keepalived:

    @staticmethod
    def tarFile():
        print("starting unpacking keepalived .......................")

        tarFilePath = cf.get("keepalived","tarFilePath")
        check = os.system("tar zxvf " + tarFilePath + " -C " + tmpPath + " > /dev/null 2>&1")

        if 0 != check:
            print("unpacking keepalived failure.............................")
            os._exit(11)

        print("done unpacking keepalived..........................")

    @staticmethod
    def make():
        print("staring make keepalived......................")

        installPath = cf.get("keepalived","installPath")
        check = os.system("cd /tmp/keepalived-* &&"
                          " ./configure --prefix=" + installPath + " > /dev/null 2>&1 &&"
                                                                   " make > /dev/null 2>&1 &&"
                                                                   " make install> /dev/null 2>&1")
        if 0 != check:
            print("make keepalived failure.............................")
            os._exit(12)

        print("done make keepalived....................................")

    @staticmethod
    def configure():
        print("starting configure keepalived............................")

        check = 0
        check += os.system("mkdir -p /etc/keepalived &&"
                          " cp ./conf/keepalived/keepalived.conf /etc/keepalived/ &&"
                          " cp ./conf/keepalived/keepalived.service /usr/lib/systemd/system/")
        #
        state = cf.get("keepalived","state")
        inetrfaceName = cf.get("keepalived","inetrfaceName")
        priority = cf.get("keepalived","priority")
        VIP = cf.get("keepalived","VIP")

        keepalived_conf_file = "/etc/keepalived/keepalived.conf"
        check += os.system("sed -i '14s#MASTER#" + state + "#' " + keepalived_conf_file)
        check += os.system("sed -i '15s#ens192#" + inetrfaceName + "#' " + keepalived_conf_file)
        check += os.system("sed -i '17s#100#" + priority + "#' " + keepalived_conf_file)
        check += os.system("sed -i '24s#172.16.6.172#" + VIP + "#' " + keepalived_conf_file)

        if 0 != check:
            print("configure keepalived failure.............................")
            os._exit(13)

        print("done configure keepalived......................................")

    @staticmethod
    def init():
        print("staring init keepalived.......................................")

        check = os.system("systemctl enable keepalived")
        if 0 != check:
            print("init keepalived failure.........................................")
            os._exit(14)

        print("done init keepalived ..............................................")



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

    #system
    system.basis()
    #system.firewall()

    #software
    keepalived.tarFile()
    keepalived.make()
    keepalived.configure()
    keepalived.init()

    os.system("rm -rf " + tmpPath + "/keepalived-*")


if __name__ == '__main__':
    integeration()