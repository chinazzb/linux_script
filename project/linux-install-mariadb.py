# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/4/18

import os
import configparser
import time

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")

systemType = cf.get("system","systemType")
systemd = cf.get("system","systemd")
installPath = cf.get("mysql","installPath")
dbDataDir = cf.get("mysql","dbDataDir")
configFilePath = cf.get("mysql","configFilePath")


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
    def firewalld():
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

    @staticmethod
    def createBasis():
        print("creating user group.......................")
        time.sleep(3)

        os.system("groupadd mysql")
        os.system("useradd -g mysql -s /sbin/nologin mysql")

        print("done created user group.......................")

class mysql:
    @staticmethod
    def tarFile():
        print("unpacking  mariadb tarball........................")
        time.sleep(3)

        tarFilePath = cf.get("mysql","tarFilePath")
        check = 0
        os.system("rm -rf " + installPath)
        check = os.system("tar zxvf " + tarFilePath + " -C /usr/local/ > /dev/null 2>&1")

        os.system("ln -sf `ls /usr/local/ | grep mariadb` " + installPath)

        print("done unpack mariadb tarball ...........................")


    @staticmethod
    def configFile():

        time.sleep(3)
        configFilePath = cf.get("mysql","configFilePath")
        os.system("mv " + configFilePath + " /etc/")

    @staticmethod
    def profile():
        print("setting profile .......................................")
        time.sleep(3)

        os.system("echo export PATH=$PATH:" + installPath + "/bin > /etc/profile.d/mysql.sh")
        os.system("source /etc/profile.d/mysql.sh")

        print("done set profile .......................................")

    @staticmethod
    def format():
        print("formatting mariadb ..................................")
        time.sleep(3)
        os.system(installPath+"/scripts/mysql_install_db --user=mysql --basedir=" + installPath + " --datadir=" + dbDataDir)
        print("done formatted mariadb.................................")

    @staticmethod
    def config_file():
        os.system("/usr/bin/cp -f " + configFilePath + " /etc/my.cnf")

        basedir = "basedir=" + installPath
        datadir = "datadir=" + dbDataDir
        #basedir
        os.system('sed -i "5c ' + basedir + '" /etc/my.cnf')
        #datadir
        os.system('sed -i "6c ' + datadir + '" /etc/my.cnf')

    @staticmethod
    def init():
        print("mariadb init.d............................")
        time.sleep(3)

        os.system("cp " + installPath + "/support-files/systemd/mariadb.service /usr/lib/systemd/system/")

        os.system("systemctl enable mariadb")
        print("done mariadb init.d.......................")



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
    system.createBasis()

    mysql.tarFile()
    mysql.profile()
    mysql.format()
    #mysql.configFile()
    mysql.init()

if __name__ == '__main__':
    integeration()