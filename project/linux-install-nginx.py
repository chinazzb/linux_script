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
import time
import configparser

cf = configparser.ConfigParser
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")

class system:
    @staticmethod
    def install_gcc():
        systemType = cf.get("system","system_type")
        check = 1
        if 'Centos' in systemType:
            print(systemType+"系统.................................")
            time.sleep(3)
            check = os.system("yum install -y gcc gcc-c++ bzip2 ")
        elif 'SUSE' in systemType:
            print(systemType+"系统.................................")
            time.sleep(3)
            check = os.system("zypper install -y gcc gcc-c++ bzip2 ")

        if 0 != check:
            print("请检查zypp源 or yum源 是否正常使用")
            os._exit(3)

    @staticmethod
    def createUserGroup():
        os.system("groupadd nginx && useradd -g web -s /bin/false nginx")
        os.system("rm -rf /tmp/nginx && mkdir -p /tmp/nginx/tar")

    @staticmethod
    def tarNginx():
        tarFilePath = cf.get("nginx","tarFilePath")
        tmpPath = cf.get("nginx","tmpPath")
        installPath = cf.get("nginx","installPath")
        os.system("rm -rf " + tmpPath + " && mkdir " +tmpPath)
        os.system("tar xvf " + tarFilePath + " -C " + tmpPath)
        os.system("for i in " + tmpPath + "/*.tar.gz;do tar zxvf $i -C " + tmpPath +";done")

class nginxConfig:

    @staticmethod
    def makeNginx():
        checkConfigure = os.system("cd /tmp/nginx/nginx-* && ./configure --user=nginx --group=nginx --prefix=/usr/local/nginx "
                                   "--with-stream --with-pcre=/tmp/nginx/pcre-8.41 --with-zlib=/tmp/nginx/zlib-1.2.11 "
                                   "--http-log-path=/var/log/nginx --error-log-path=/var/log/nginx")
        if 0 != checkConfigure:
            print("configure nginx fatal error.................................")
            os._exit(10)
        checkMake = os.system("cd /tmp/nginx/nginx*/ && make && make install")
        if 0 != checkMake:
            print("make nginx fatal error.......................................")
            os._exit(11)

    @staticmethod
    def softwConnect():
        checkNginxPath = os.path.exists("/usr/local/nginx/")
        if not checkNginxPath:
            print(" not be found '/usr/local/nginx' ")
            os._exit(12)

        os.system(" ln -s /usr/local/nginx/conf /etc/nginx ")

    @staticmethod
    def serviceFile():
        os.system("mv /tmp/nginx/nginx")


def installNginx():
    system.zypper()
    system.createUserGroup()
    system.tarNginx()
    nginxConfig.makeNginx()
    nginxConfig.softwConnect()

if __name__ == '__main__':
    installNginx()