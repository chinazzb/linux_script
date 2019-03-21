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

tomcatTar = cf.get("tomcat","tarFilePath")
tomcatTmpPath = cf.get("tomcat","tmpPath")
tomcatApr = tomcatTmpPath + "/tomcat-apr"
tomcatInstallPath = cf.get("tomcat","installPath")
jdkInstallPath = cf.get("java","jdkInstallPath")


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
    def tarz_tomcat():
        if not os.path.exists(tomcatTar):
            print('请检查配置文件,[tomcat]子项下的 "tomcatFilePath" 是否存在')
            os._exit(4)
        #tmp dir
        os.system("mv " + tomcatTmpPath + " /tmp/tomcatBak")
        os.system("mkdir " + tomcatTmpPath)
        os.system("tar xvf " + tomcatTar + " -C " + tomcatTmpPath)
        os.system("for i in " + tomcatApr + "/*.tar.gz;do tar zxvf $i -C " + tomcatTmpPath + ";done")
        os.system("tar xvf " + tomcatApr + "/expat* -C " + tomcatTmpPath)

    @staticmethod
    def jdk_configure():
        jdkPath = tomcatTmpPath
        os.system("rm -rf " + jdkInstallPath)
        os.system("mkdir " + jdkInstallPath)
        os.system("mv " + jdkPath + "/jdk* " + jdkInstallPath)
        jdkHome = jdkInstallPath + "".join(os.listdir(jdkInstallPath))
        #检查是否已经配置javahome
        print("开始配置JAVAHOME....................................")
        time.sleep(3)
        checkJavaHome = os.system("cat /etc/profile | grep JAVA_HOME > /dev/null")
        if 0 != checkJavaHome:
            profile = open("/etc/profile","a")
            profile.write("JAVA_HOME=" + jdkHome + "\n")
            profile.write("JRE_HOME=$JAVA_HOME/jre\n")
            profile.write("CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib\n")
            profile.write("LD_LIBRARY_PATH=/usr/local/apr/lib:$LD_LIBRARY_PATH\n")
            profile.write("PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin\n")
            profile.write("export JAVA_HOME JRE_HOME PATH CLASSPATH LD_LIBRARY_PATH\n")
            profile.close()
            print("JAVAHOME已配置完毕")
        else:
            print("JAVAHOME已存在无需配置....................................")

    @staticmethod
    def system_firewalld():
        #openPort = cf.get("system","openPort")
        firewallPort= 'FW_SERVICES_EXT_TCP="80 22"'
        os.system("service SuSEfirewall2_setup start")
        os.system("service SuSEfirewall2_init start")
        replace('/etc/sysconfig/SuSEfirewall2','FW_SERVICES_EXT_TCP=""',firewallPort)
        os.system("chkconfig SuSEfirewall2_setup on")
        os.system("chkconfig SuSEfirewall2_init on")
        os.system("service SuSEfirewall2_setup restart")
        os.system("service SuSEfirewall2_init restart")
        print("防火墙配置成功.................................................................")
        print("此服务器仅开放8080 22 端口,若需调整请联系系统维护人员..............................")


class software:
    @staticmethod
    def make_tomcat_apr():
        print("开始编译tomcat及依赖包.........................................................")
        time.sleep(3)
        #tomcat
        replace(tomcatTmpPath + "/apr-1.6.5/configure","RM='$RM'","RM='$RM -f'")
        #make
        print("开始编译apr............................................................")
        time.sleep(3)
        checkApr = os.system("cd " + tomcatTmpPath + "/apr-* && ./configure --prefix=/usr/local/apr/ && make && make install")
        if 0 != checkApr:
            print("编译apr失败请检查相对应文件")
            os._exit(11)
        print("apr编译安装完成..........................................................")

    @staticmethod
    def make_tomcat_apr_iconv():
        print("开始编译apr-iconv.......................................................")
        time.sleep(3)
        checkAprIconv = os.system("cd "+ tomcatTmpPath + "/apr-iconv* && ./configure --prefix=/usr/local/apr-iconv/ "
                                                         "--with-apr=/usr/local/apr && make && make install")
        if 0 != checkAprIconv:
            print("编译apr-iconv失败请检查相对应文件")
            os._exit(12)
        print("apr-iconv编译安装完成...................................................")

    @staticmethod
    def make_expat():
        print("开始编译expat..........................................................")
        time.sleep(3)
        checkExpat = os.system("cd " + tomcatTmpPath + "/expat* && ./configure --prefix=/usr/local/expat && make && make install ")
        if 0 != checkExpat:
            print("编译expat文件失败请检查依赖项")
            os._exit(13)
        print("expat编译安装完成......................................................")

    @staticmethod
    def make_tomcat_apr_util():
        print("开始编译apr-util.......................................................")
        time.sleep(3)
        checkAprUtil = os.system("cd " + tomcatTmpPath + "/apr-util* && ./configure --prefix=/usr/local/apr-util"
                                                         " --with-apr=/usr/local/apr --with-apr-iconv=/usr/local/apr-iconv/bin/apriconv"
                                                         " --with-expat=/usr/local/expat && make && make install")
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
        checkTomcatNative = os.system("cd " + tomcatTmpPath + "/apache-tomcat-*/bin/ && tar zxvf tomcat-native.tar.gz && "
                                      "cd tomcat-native-*/native && ./configure --with-apr=/usr/local/apr/bin/apr-1-config "
                                      "--with-java-home=" + jdkHome + " && make && make install")
        if 0 != checkTomcatNative:
            print("TomcatNative编译失败，请检查对应路径")
            os._exit(14)
        print("TomcatNative编译安装完成............................................................")

    @staticmethod
    def install_tomcat():
        print("安装 tomcat...................................................................")
        time.sleep(3)
        installPath = cf.get("tomcat","installPath")

        os.system("cp -R /usr/local/apr/lib/* /usr/lib64 && cp -R /usr/local/apr/lib/* /usr/lib")
        os.system("mv /tmp/tomcat/apache-tomcat* /usr/local/ && ln -s /usr/local/apache-tomcat* " + installPath)
        os.system("ln -s " + installPath + "/conf /etc/tomcat && ln -s " + installPath + "/logs " + "/var/log/tomcat")
        print("install tomcat done.................................................................")

    @staticmethod
    def optimization_tomcat():
        time.sleep(3)
        print("starting tomcat optimization......................................................")
        minThread = '"minSpareThreads=" '+ cf.get("tomcat","minThread") + '"'
        maxThread = '"maxThreads="'+ cf.get("tomcat","maxThread") + '"'
        replace("/etc/tomcat/server.xml",'minSpareThreads="400"',minThread)
        replace("/etc/tomcat/server.xml",'maxThreads="1000"',maxThread)
        tomcatProject = tomcatInstallPath + "/webapps/"

        os.system("mv  " + tomcatApr + "/server.xml /etc/tomcat/")
        os.system("mv  " + tomcatApr + "/tomcat-users.xml /etc/tomcat/")
        os.system("rm -rf " + tomcatProject + " && mv  " + tomcatApr + "/manager/ " + tomcatProject)
        os.system("chown -hR tomcat:web {/usr/local/apache-tomcat*," + tomcatInstallPath + "}" )
        print("tomcat optimization done...........................................................")

    @staticmethod
    def enable_tomcat():
        os.system("cp " + tomcatApr + "/tomcat /etc/init.d/tomcat && chmod 755 /etc/init.d/tomcat")
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
    system.install_gcc()
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

if __name__ == '__main__':
    integeration()