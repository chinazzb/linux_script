# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date:
#version: 0.9

#SUSE11

import os
import time
import configparser


cf = configparser.ConfigParser()
configFilePath = "./install.conf"
cf.read(configFilePath,encoding="utf-8-sig")

tarFilesPath = cf.get("tomcat", "tarFilesPath")
tmpPath = cf.get("tomcat","tmpPath")
installPath = cf.get("tomcat", "installPath")
jdkInstallPath = cf.get("java","installPath")
systemType = cf.get("system","systemType")


class system:

    @staticmethod
    def basis():
        hostName = cf.get("system","hostName")
        check = 1
        if 'Centos' in systemType or 'Redhat'in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check += os.system("yum install -y gcc gcc-c++ > /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/hostname")

        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check += os.system("zypper install -y gcc gcc-c++ > /dev/null 2>&1")
            #modify host namem
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/HOSTNAME")

        if 0 != check:
            print("check zypp or yum repo")
            os._exit(3)

    @staticmethod
    def firewalld():
        openPortList = cf.get("system","openPort")
        openPortListSplit = str(openPortList).split(" ")
        #Centos Redhat
        if 'Centos' in systemType or 'Redhat' in systemType:
            os.system("systemctl start firewalld")
            os.system("systemctl enable firewalld")
            for i in range(len(openPortListSplit)):
                os.system("firewall-cmd --permanent --zone=public --add-port="+openPortListSplit[i]+"/tcp ")
            os.system("firewall-cmd --reload")
        elif 'SUSE' in systemType:
            firewallFile ="/etc/sysconfig/SuSEfirewall2"
            replace(firewallFile,'FW_SERVICES_EXT_TCP=""','FW_SERVICES_EXT_TCP="'+openPortList+'"')
            os.system("rcSuSEfirewall2 start")
            os.system("chkconfig SuSEfirewall2_init on")
            os.system("chkconfig SuSEfirewall2_setup on")


class software:

    @staticmethod
    def tarz_tomcat():
        if not os.path.exists(tarFilesPath):
            print('check install.conf [tomcat] "tarFilesPath" does it exist')
            os._exit(4)

        #tmp dir
        check = 0
        check += os.system(" rm -rf " + tmpPath + " && mkdir " + tmpPath)
        check += os.system("for i in `ls " + tarFilesPath + "/*.tar.gz | grep -v jdk`; do tar zxvf $i -C " + tmpPath + " > /dev/null 2>&1;done")
        check += os.system("tar xvf " + tarFilesPath + "/expat* -C " + tmpPath + " > /dev/null 2>&1")
        if 0 != check:
            print("unzip tomcat failure .........................................................")

    @staticmethod
    def jdk_configure():
        os.system("rm -rf " + jdkInstallPath)
        os.system("mkdir " + jdkInstallPath)
        os.system("tar zxvf " + tarFilesPath + "/jdk* -C " + jdkInstallPath + " > /dev/null 2>&1")
        jdkHome = jdkInstallPath + "".join(os.listdir(jdkInstallPath))
        #检查是否已经配置javahome
        print("starting configure JAVAHOME....................................")
        time.sleep(3)
        checkJavaHome = os.system("cat /etc/profile.d/jdkHome.sh | grep JAVA_HOME > /dev/null 2>&1")
        if 0 != checkJavaHome:
            profile = open("/etc/profile.d/jdkHome.sh","a")
            profile.write("JAVA_HOME=" + jdkHome + "\n")
            profile.write("JRE_HOME=$JAVA_HOME/jre\n")
            profile.write("CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib\n")
            profile.write("LD_LIBRARY_PATH=/usr/local/apr/lib:$LD_LIBRARY_PATH\n")
            profile.write("CATALINA_HOME=" + installPath + "\n")
            profile.write("CATALINA_BASE=" + installPath + "\n")
            profile.write("PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin\n")
            profile.write("export JAVA_HOME JRE_HOME PATH CLASSPATH LD_LIBRARY_PATH\n")
            profile.close()
            print("JAVAHOME configured done")
        else:
            print("JAVAHOME exist")

    @staticmethod
    def make_tomcat_apr():
        print("starting make apr............................................................")

        time.sleep(5)
        checkApr = os.system('sed -i "#RM=\'$RM\'#RM=\'$RM -f\'#" ' + tmpPath + '/apr-*/configure')
        #make
        time.sleep(3)
        checkApr += os.system("cd " + tmpPath + "/apr-*"
                                                     " && ./configure --prefix=/usr/local/apr/ > /dev/null 2>&1"
                                                     " && make > /dev/null 2>&1"
                                                     " && make install > /dev/null 2>&1")
        if 0 != checkApr:
            print("make apr failure ..................................")
            os._exit(11)

        print("make apr done..........................................................")

    @staticmethod
    def make_tomcat_apr_iconv():
        print("starting make apr-iconv.......................................................")
        time.sleep(3)
        checkAprIconv = os.system("cd "+ tmpPath + "/apr-iconv*"
                                                         " && ./configure --prefix=/usr/local/apr-iconv/"
                                                         " --with-apr=/usr/local/apr > /dev/null 2>&1"
                                                         " && make > /dev/null 2>&1"
                                                         " && make install  > /dev/null 2>&1")
        if 0 != checkAprIconv:
            print("make apr-iconv failure .....................................")
            os._exit(12)
        print("make apr-iconv done...................................................")

    @staticmethod
    def make_expat():
        print("staring make expat..........................................................")
        time.sleep(3)
        checkExpat = os.system("cd " + tmpPath + "/expat*"
                                                       " && ./configure --prefix=/usr/local/expat > /dev/null 2>&1"
                                                       " && make > /dev/null 2>&1"
                                                       " && make install > /dev/null 2>&1")
        if 0 != checkExpat:
            print("make expat failure")
            os._exit(13)
        print("make expat done......................................................")

    @staticmethod
    def make_tomcat_apr_util():
        print("staring ake apr-util.......................................................")
        time.sleep(3)
        checkAprUtil = os.system("cd " + tmpPath + "/apr-util* "
                                                         " && ./configure --prefix=/usr/local/apr-util"
                                                         " --with-apr=/usr/local/apr"
                                                         " --with-apr-iconv=/usr/local/apr-iconv/bin/apriconv"
                                                         " --with-expat=/usr/local/expat > /dev/null 2>&1"
                                                         " && make > /dev/null 2>&1"
                                                         " && make install  > /dev/null 2>&1")
        if 0 != checkAprUtil:
            print("make apr-util failure")
            os._exit(14)
        print("make apr-util done.......................................................")

    @staticmethod
    def make_tomcatNative():
        print("staring make TomcatNative.......................................................")

        jdkHome = jdkInstallPath + "".join(os.listdir(jdkInstallPath))
        time.sleep(3)
        check = 0
        check += os.system("groupadd tomcat && useradd -g tomcat -s /sbin/nologin -M tomcat")
        check += os.system("cd " + tmpPath + "/apache-tomcat-*/bin/"
                                                              " && tar zxvf tomcat-native.tar.gz > /dev/null 2>&1"
                                                              " && cd tomcat-native-*/native"
                                                              " && ./configure --with-apr=/usr/local/apr/bin/apr-1-config"
                                                              " --with-java-home=" + jdkHome + " > /dev/null 2>&1 "
                                                              " && make > /dev/null 2>&1"
                                                              " && make install  > /dev/null 2>&1")
        if 0 != check:
            print("make TomcatNative failure.......................................................")
            os._exit(14)

        print("make TomcatNative done............................................................")

    @staticmethod
    def install_tomcat():
        print("starting install tomcat...................................................................")

        time.sleep(3)
        check = 0
        checkAprSoftLink = os.system("cp -R /usr/local/apr/lib/* /usr/lib64  &&"
                                    " cp -R /usr/local/apr/lib/* /usr/lib")

        check += os.system("rm -rf " + installPath)
        #soft link
        check += os.system("mv /tmp/tomcat/apache-tomcat* /usr/local/")
        check += os.system("ln -s /usr/local/apache-tomcat* " + installPath)
        check += os.system("rm -rf /etc/tomcat &&"
                  " ln -s /usr/local/apache-tomcat*/conf /etc/tomcat")

        check += os.system("rm -rf /var/log/tomcat  &&"
                  " ln -s /usr/local/apache-tomcat*/logs /var/log/tomcat")
        if 0 != check:
            print("install tomcat failure..................................................")

        print("install tomcat done.................................................................")

    @staticmethod
    def optimization_tomcat():
        time.sleep(3)
        print("starting tomcat optimization......................................................")

        #server
        os.system("rm -rf /etc/tomcat/server.xml")
        os.system("cp ./conf/tomcat/server.xml /etc/tomcat/")

        minThread = 'minSpareThreads=" '+ cf.get("tomcat","minThread") + '"'
        maxThread = 'maxThreads="'+ cf.get("tomcat","maxThread") + '"'
        replace("/etc/tomcat/server.xml",'minSpareThreads="400"',minThread)
        replace("/etc/tomcat/server.xml",'maxThreads="1000"',maxThread)
        tomcatProject = installPath + "/webapps/"

        #tomcat-users
        os.system("rm -rf /etc/tomcat/tomcat-users.xml")
        os.system("cp ./conf/tomcat/tomcat-users.xml /etc/tomcat/")

        #tomcat manager
        os.system("rm -rf " + tomcatProject + "/*")
        os.system("cp -r ./conf/tomcat/manager/ " + tomcatProject)
        os.system("chown -hR tomcat:tomcat {/usr/local/apache-tomcat*," + installPath + "}")

        print("tomcat optimization done...........................................................")

    @staticmethod
    def enable_tomcat():
        systemd = cf.get("system","systemd")
        check = 0

        if "0" in systemd:
            check += os.system("cp ./conf/tomcat/tomcat.init /etc/init.d/tomcat")
            check += os.system("chmod 755 /etc/init.d/tomcat")
        else:
            check += os.system("cp ./conf/tomcat/tomcat /etc/sysconfig/tomcat")
            check += os.system("cp ./conf/tomcat/tomcat.service /usr/lib/systemd/system/")

        check += os.system("chkconfig tomcat on")

        if 0 != check:
            print("init.d tomcat failure ......................................")
        time.sleep(6)
        print("done init.d tomcat...........................................................")



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
    system.firewalld()


    #software
    software.tarz_tomcat()
    software.jdk_configure()
    software.make_tomcat_apr()
    software.make_tomcat_apr_iconv()
    software.make_expat()
    software.make_tomcat_apr_util()
    software.make_tomcatNative()
    software.install_tomcat()
    software.optimization_tomcat()
    software.enable_tomcat()

    print("clean all................................................")
    os.system("rm -rf  " + tmpPath)

if __name__ == '__main__':
    integeration()