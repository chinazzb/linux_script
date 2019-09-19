# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 06-12-2018
#version: 0.9


#linux Centos Redhat SUSE


import os
import time
import configparser

cf = configparser.ConfigParser()
confFilePath = "./install.conf"
cf.read(confFilePath,encoding="utf-8-sig")

tarFilesPath = cf.get("nginx","tarFilesPath")
tmpPath = cf.get("nginx","tmpPath")
systemType = cf.get("system","systemType")
systemd = cf.get("system","systemd")

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
    def createUserGroup():
        os.system("groupadd nginx")
        os.system("useradd -g nginx -s /bin/false nginx")

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



class nginxConfig:

    @staticmethod
    def tarNginx():

        os.system("rm -rf " + tmpPath + " && mkdir " + tmpPath)
        os.system("for i in " + tarFilesPath + "/*; do tar zxvf $i -C " + tmpPath + "; done")

    @staticmethod
    def makeNginx():
        print("starting make nginx ..............................................")

        nginxInstllPath = cf.get("nginx","installPath")
        os.system("rm -rf " + nginxInstllPath)
        checkConfigure = os.system("cd " + tmpPath +"/nginx-* && ./configure --user=nginx --group=nginx"
                                                    " --prefix=" + nginxInstllPath +
                                                    " --with-stream"
                                                    " --with-pcre=" + tmpPath + "/pcre-8.43"
                                                    " --with-zlib=" + tmpPath + "/zlib-1.2.11 > /dev/null 2>&1")
        if 0 != checkConfigure:
            print("configure nginx fatal error.................................")
            os._exit(10)

        checkMake = os.system("cd " + tmpPath + "/nginx*/ "
                                                " && make > /dev/null 2>&1"
                                                " && make install  > /dev/null 2>&1")

        if 0 != checkMake:
            print("make nginx fatal error.......................................")
            os._exit(11)

        print("starting make nginx ............................................")

    @staticmethod
    def optimization():
        print("start optimization nginx .........................")
        time.sleep(3)
        nginxInstall = cf.get("nginx","installPath")
        nginxConfigPath= nginxInstall+"/conf"

        #soft link
        print("create soft link nginx ........................")
        time.sleep(2)
        os.system("rm -f /etc/nginx")
        os.system("ln -s " + nginxConfigPath + " /etc/nginx")
        os.system("rm -rf " + nginxConfigPath + "/nginx.conf ")
        os.system("cp ./conf/nginx/nginx.conf " + nginxConfigPath)
        print("create soft link nginx done ....................")


        #nginx init.d
        print("create nginx init.d............................")
        time.sleep(2)
        if "Centos" in systemType or 'Redhat'in systemType:
            if "0" in systemd:
                os.system("mv ./conf/nginx/nginx /etc/init.d/")
                os.system("chmod 755 /etc/init.d/nginx")
            else:
                os.system("mv ./conf/nginx/nginx.service /usr/lib/systemd/system/")
        elif "SUSE" in systemType:
            if "0" in systemd:
                os.system("mv ./conf/nginx/nginx /etc/init.d/")
                os.system("chmod 755 /etc/init.d/nginx")
            else:
                os.system("mv ./conf/nginx/nginx.service /usr/lib/systemd/system/")

        os.system("chkconfig nginx on")
        print("nginx init.d done............................")


        #nginx port
        print("configure nginx port .........................")
        time.sleep(2)
        port = cf.get("nginx","port")
        port = "listen " + port
        replace(nginxConfigPath + "/nginx.conf","listen 80",port)
        print("configure nginx port done.....................")


        #worker_processes
        print("configure nginx worker_processes .........................")
        time.sleep(2)
        worker_processes = cf.get("nginx","worker_processes")
        replace(nginxConfigPath + "/nginx.conf" ,"worker_processes 2","worker_processes " + worker_processes)
        print("configure nginx worker_processes done.....................")


        #worker_connections
        print("configure nginx worker_connections .....................")
        time.sleep(2)
        worker_connections = cf.get("nginx","worker_connections")
        replace(nginxConfigPath + "/nginx.conf","worker_connections  1024","worker_connections " + worker_connections)
        print("configure nginx worker_connections done.....................")


        #proxy tomcat
        print("configure nginx upstream server .....................")
        time.sleep(2)
        proxyTomcatList = cf.get("nginx","proxyTomcat")
        proxyTomcatListSplit = str(proxyTomcatList).split(",")
        for i in range(len(proxyTomcatListSplit)):
            os.system("sed -i '43a\ \tserver " + proxyTomcatListSplit[i] + ";' " + nginxConfigPath + "/nginx.conf")
        print("configure nginx upstream server done .................")

        #project type
        print("configure nginx upstream project type .....................")
        time.sleep(2)
        projectTypeList = cf.get("project","projectType")
        projectTypeListSplit = str(projectTypeList).split(",")
        if 1 == len(projectTypeListSplit):
            replace(nginxConfigPath+"/nginx.conf","largecash",projectTypeList)
        else:
            print("目前只允许填写单个项目,此项不做操作，继续允许下一步.请手动配置")
        print("configure nginx upstream project type done.......................")

        print("optimization nginx done................................")

#replace file string
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
    system.createUserGroup()
    system.firewalld()


    nginxConfig.tarNginx()
    nginxConfig.makeNginx()
    nginxConfig.optimization()
    os.system("rm -rf " + tmpPath)


if __name__ == '__main__':
    integeration()