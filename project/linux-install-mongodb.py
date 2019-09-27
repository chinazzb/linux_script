# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/9/25


import os
import configparser
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
        check = 1
        if 'Centos' in systemType or 'Redhat'in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("yum install -y gcc gcc-c++ > /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/hostname")

        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("zypper install -y gcc gcc-c++ > /dev/null 2>&1")
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
                          "--add-port=" + openPortListSplit[i] + "/tcp >/dev/null 2>&1")
            os.system("firewall-cmd --reload")
        elif 'SUSE' in systemType:
            firewallFile ="/etc/sysconfig/SuSEfirewall2"
            replace(firewallFile,'FW_SERVICES_EXT_TCP=""','FW_SERVICES_EXT_TCP="' + openPortList + '"')
            os.system("rcSuSEfirewall2 start")
            os.system("chkconfig SuSEfirewall2_init on")
            os.system("chkconfig SuSEfirewall2_setup on")

    print("done configure system firewalld")


class mongodb:
    @staticmethod
    def tarFile():
        print("staring unpacking mongodb.........................................")
        systemType =  cf.get("system","systemType")
        if "Centos" in systemType or "Redhat" in systemType:
            systemType = "RHEL"
        tarFilePath = cf.get("mongodb","tarFilePath")

        check = os.system("tar zxvf ./software/`ls ./software/ | grep mongodb | grep -i " + systemType + "`  -C /usr/local/ > /dev/null 2>&1")
        check += os.system("ln -sf `ls /usr/local/ | grep mongodb` " + installPath)

        if 0 != check:
            print("unpacking mongodb failure..........................................")
            os._exit(11)

        print("done unpacking mongodb............................................")

    @staticmethod
    def profile():
        print("staring create profile.......................................")
        time.sleep(3)
        check = os.system("echo export PATH=$PATH:" + installPath + "/bin > /etc/profile.d/mongodb.sh")

        if 0 != check:
            print("create profile failure ............................................")
            os._exit(12)


    @staticmethod
    def format():
        print("staring format mongodb.............................")

        check = os.system("groupadd mongod"
                          " && useradd -g mongod -s /sbin/nologin mongod")

        logPath = cf.get("mongodb","logPath")
        check += os.system("mkdir -p " + logPath +
                           " && chown mongod:mongod " + logPath)
        if 0 != check:
            print("create format failure .........................................")
            os._exit(13)
        print("done format mongodb.............................................")


    @staticmethod
    def configure():
        print("staring configure mongodb.....................................")

        dbPath = cf.get("mongodb","dbPath")
        check = os.system("cp ./conf/mongodb/mongod.conf /etc/")
        check += os.system("mkdir -p " + dbPath +
                            " && /usr/bin/chown mongod:mongod " + dbPath +
                            " && sed -i '14s#/var/lib/mongo#" + dbPath + "#' /etc/mongod.conf")

        bindIp = cf.get("mongodb","bindIp")
        check += os.system("sed -i '29s#127.0.0.1#" + bindIp + "#' /etc/mongod.conf")

        if 0 != check:
            print("configure mongodb failure .................................")
            os._exit(14)

        print("done configure mongodb ........................................")

    @staticmethod
    def init():
        print("staring init.d mongodb.......................................")

        check = os.system("cp ./conf/mongodb/mongod.service /usr/lib/systemd/system/ && systemctl enable mongod")

        if 0 != check:
            print("init.d mongodb failure .......................................")
            os._exit(15)

        print("done init.d mongodb........................................")

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

    mongodb.tarFile()
    mongodb.profile()
    mongodb.format()
    mongodb.configure()
    mongodb.init()

if __name__ == '__main__':
    integeration()