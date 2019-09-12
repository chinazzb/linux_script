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
            check = os.system("yum install -y gcc gcc-c++ > /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/hostname")

        elif 'SUSE' in systemType:
            print(systemType + " system.................................")
            time.sleep(3)
            check = os.system("zypper install -y gcc gcc-c++ /dev/null 2>&1")
            #modify host name
            os.system("sysctl -w kernel.hostname=" + hostName + " && hostname > /etc/HOSTNAME")

        if 0 != check:
            print("请检查zypp源 or yum源 是否正常使用")
            os._exit(3)

    @staticmethod
    def tarz_tomcat():
        tomcatTarMD5 = "535d83309fd8109f064048b831fd3c9e"
        if not os.path.exists(tarFilesPath):
            print('请检查配置文件,[tomcat]子项下的 "tomcatFilePath" 是否存在')
            os._exit(4)

        #tmp dir
        check = 0
        check += os.system("mkdir " + tmpPath)
        check += os.system("for i in `ls " + tarFilesPath + "/*.tar.gz | grep -v jdk`; do tar zxvf $i -C " + tmpPath + " > /dev/null 2>&1;done")
        check += os.system("tar xvf " + tarFilesPath + "/expat* -C " + tmpPath + " > /dev/null 2>&1")
        if 0 != check:
            print("unzip tomcat-apr.tar fatal................................")

    @staticmethod
    def jdk_configure():
        os.system("rm -rf " + jdkInstallPath)
        os.system("mkdir " + jdkInstallPath)
        os.system("tar zxvf " + tarFilesPath + "/jdk* -C " + jdkInstallPath)
        jdkHome = jdkInstallPath + "".join(os.listdir(jdkInstallPath))
        #检查是否已经配置javahome
        print("开始配置JAVAHOME....................................")
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
            print("JAVAHOME已配置完毕")
        else:
            print("JAVAHOME已存在无需配置....................................")

    @staticmethod
    def system_firewalld():
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
    def make_tomcat_apr():
        print("开始编译tomcat及依赖包.........................................................")
        time.sleep(3)
        #tomcat
        os.system("sed -i #RM='$RM'#RM='$RM -f'# " + tmpPath + "/apr-*/configure")
        #make
        print("开始编译apr............................................................")
        time.sleep(3)
        checkApr = os.system("cd " + tmpPath + "/apr-*"
                                                     " && ./configure --prefix=/usr/local/apr/ > /dev/null 2>&1"
                                                     " && make > /dev/null 2>&1"
                                                     " && make install > /dev/null 2>&1")
        if 0 != checkApr:
            print("编译apr失败请检查相对应文件")
            os._exit(11)
        print("apr编译安装完成..........................................................")

    @staticmethod
    def make_tomcat_apr_iconv():
        print("开始编译apr-iconv.......................................................")
        time.sleep(3)
        checkAprIconv = os.system("cd "+ tmpPath + "/apr-iconv*"
                                                         " && ./configure --prefix=/usr/local/apr-iconv/"
                                                         " --with-apr=/usr/local/apr > /dev/null 2>&1"
                                                         " && make > /dev/null 2>&1"
                                                         " && make install  > /dev/null 2>&1")
        if 0 != checkAprIconv:
            print("编译apr-iconv失败请检查相对应文件")
            os._exit(12)
        print("apr-iconv编译安装完成...................................................")

    @staticmethod
    def make_expat():
        print("开始编译expat..........................................................")
        time.sleep(3)
        checkExpat = os.system("cd " + tmpPath + "/expat*"
                                                       " && ./configure --prefix=/usr/local/expat > /dev/null 2>&1"
                                                       " && make > /dev/null 2>&1"
                                                       " && make install > /dev/null 2>&1")
        if 0 != checkExpat:
            print("编译expat文件失败请检查依赖项")
            os._exit(13)
        print("expat编译安装完成......................................................")

    @staticmethod
    def make_tomcat_apr_util():
        print("开始编译apr-util.......................................................")
        time.sleep(3)
        checkAprUtil = os.system("cd " + tmpPath + "/apr-util* "
                                                         " && ./configure --prefix=/usr/local/apr-util"
                                                         " --with-apr=/usr/local/apr"
                                                         " --with-apr-iconv=/usr/local/apr-iconv/bin/apriconv"
                                                         " --with-expat=/usr/local/expat > /dev/null 2>&1"
                                                         " && make > /dev/null 2>&1"
                                                         " && make install  > /dev/null 2>&1")
        if 0 != checkAprUtil:
            print("编译apr-util失败请检查相对应文件")
            os._exit(14)
        print("apr-util编译安装完成.......................................................")

    @staticmethod
    def make_tomcatNative():
        jdkHome = jdkInstallPath + "".join(os.listdir(jdkInstallPath))
        print("开始编译TomcatNative.......................................................")
        time.sleep(3)
        os.system("groupadd web && useradd -g web -s /bin/false -M tomcat")
        checkTomcatNative = os.system("cd " + tmpPath + "/apache-tomcat-*/bin/"
                                                              " && tar zxvf tomcat-native.tar.gz > /dev/null 2>&1"
                                                              " && cd tomcat-native-*/native"
                                                              " && ./configure --with-apr=/usr/local/apr/bin/apr-1-config"
                                                              " --with-java-home=" + jdkHome + " > /dev/null 2>&1 "
                                                              " && make > /dev/null 2>&1"
                                                              " && make install  > /dev/null 2>&1")
        if 0 != checkTomcatNative:
            print("TomcatNative编译失败，请检查对应路径")
            os._exit(14)
        print("TomcatNative编译安装完成............................................................")

    @staticmethod
    def install_tomcat():
        print("安装 tomcat...................................................................")
        time.sleep(3)
        check = 1
        checkAprSoftLink = os.system("cp -R /usr/local/apr/lib/* /usr/lib64"
                                    " && cp -R /usr/local/apr/lib/* /usr/lib")

        os.system("rm -rf " + installPath)
        #soft link
        os.system("mv /tmp/tomcat/apache-tomcat* /usr/local/")
        os.system("ln -s /usr/local/apache-tomcat* " + installPath)
        os.system("rm -rf /etc/tomcat"
                  " && ln -s /usr/local/apache-tomcat*/conf /etc/tomcat")

        os.system("rm -rf /var/log/tomcat"
                  " && ln -s /usr/local/apache-tomcat*/logs /var/log/tomcat")
        print("install tomcat done.................................................................")

    @staticmethod
    def optimization_tomcat():
        time.sleep(3)
        print("starting tomcat optimization......................................................")

        #server
        os.system("rm -rf /etc/tomcat/server.xml")
        os.system("mv  " + tmpPath + "/tomcat-apr/server.xml /etc/tomcat/")

        minThread = 'minSpareThreads=" '+ cf.get("tomcat","minThread") + '"'
        maxThread = 'maxThreads="'+ cf.get("tomcat","maxThread") + '"'
        replace("/etc/tomcat/server.xml",'minSpareThreads="400"',minThread)
        replace("/etc/tomcat/server.xml",'maxThreads="1000"',maxThread)
        tomcatProject = installPath + "/webapps/"

        #tomcat-users
        os.system("rm -rf /etc/tomcat/tomcat-users.xml")
        os.system("mv  " + tmpPath + "/tomcat-apr/tomcat-users.xml /etc/tomcat/")

        #tomcat manager
        os.system("rm -rf " + tomcatProject+"*")
        os.system("cp -r " + tmpPath + "/tomcat-apr/manager/ " + tomcatProject)
        os.system("chown -hR tomcat:web {/usr/local/apache-tomcat*," + installPath + "}")

        print("tomcat optimization done...........................................................")

    @staticmethod
    def enable_tomcat():
        os.system("cp " + tmpPath + "/tomcat-apr/tomcat /etc/init.d/tomcat")
        os.system("chmod 755 /etc/init.d/tomcat")
        os.system("chkconfig tomcat on")
        time.sleep(6)
        print("完成tomcat自启动...........................................................")



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
    system.tarz_tomcat()
    system.jdk_configure()

    #software
    software.make_tomcat_apr()
    software.make_tomcat_apr_iconv()
    software.make_expat()
    software.make_tomcat_apr_util()
    software.make_tomcatNative()
    software.install_tomcat()
    software.optimization_tomcat()
    software.enable_tomcat()

    print("clean all")
    os.system("rm -rf  " + tmpPath)

if __name__ == '__main__':
    integeration()