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
    def zypper():
        checkzypper = os.system("zypper install -y gcc gcc-c++")
        if 0!= checkzypper:
            print("zypper fatal error...................................")
            os._exit(1)
    @staticmethod
    def createUserGroup():
        os.system("groupadd web && useradd -g web -s /bin/false nginx")
        os.system("rm -rf /tmp/nginx && mkdir -p /tmp/nginx/tar")

    @staticmethod
    def tarNginx():
        nginxName = "nginx.tar"
        nginxPath = ""
        while True:
            nginxPath = raw_input("input absolute path to the nginx Tar File:")
            if os.path.exists(nginxPath):
                break

        os.system("tar xvf " + nginxPath +"/" + nginxName + " -C /tmp/nginx/tar")
        os.system("for i in /tmp/nginx/tar/*.tar.gz;do tar zxvf $i -C /tmp/nginx/;done")





class nginxConfig:

    @staticmethod
    def makeNginx():
        checkConfigure = os.system("cd /tmp/nginx/nginx-* && ./configure --user=nginx --group=web --prefix=/usr/local/nginx "
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