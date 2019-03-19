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
configFilePath = "../test/test.ini"
cf.read(configFilePath,encoding="utf-8-sig")


class system:

    @staticmethod
    def install_gcc():
        check = os.system("zypper install -y gcc gcc-c++ bzip2 ")
        if 0 != check:
            print("请检查zypp源是否正常使用")
            os._exit(3)

    @staticmethod
    def tarz_tomcat():
        tomcatTar = cf.get("tomcat","tarFilePath")
        if not os.path.exists(tomcatTar):
            print("check this path,the path dones not exist")
            tomcatTar = raw_input("请输入tomcat-apr.tar此文件的绝对路径:")
            #tmp dir
            os.system("mv /tmp/tomcat /tmp/tomcatBak")
            os.system("mkdir /tmp/tomcat")
            tomcat = "/tmp/tomcat"
            os.system("tar xvf " + tomcatTar + " -C " + tomcat)
            tomcatApr = tomcat+"/tomcat-apr"
            os.system("for i in " + tomcatApr + "/*.tar.gz;do tar zxvf $i -C /tmp/tomcat/;done")
            os.system("tar xvf " + tomcatApr + "/expat* -C /tmp/tomcat/")
            return tomcatApr

    @staticmethod
    def jdk_configure():
        os.system("rm -rf /usr/java/")
        os.system("mkdir /usr/java/")
        os.system("mv /tmp/tomcat/jdk* " + cf.get("java","jdkInstallPath"))
        jdkHome = "/usr/java/"+"".join(os.listdir("/usr/java/"))
        profile = open("/etc/profile","a")
        profile.write("JAVA_HOME=" + jdkHome + "\n")
        profile.write("JRE_HOME=$JAVA_HOME/jre\n")
        profile.write("CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib\n")
        profile.write("LD_LIBRARY_PATH=/usr/local/apr/lib:$LD_LIBRARY_PATH\n")
        profile.write("PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin\n")
        profile.write("export JAVA_HOME JRE_HOME PATH CLASSPATH LD_LIBRARY_PATH\n")
        profile.close()
        return jdkHome



class make_tomcat:
    def make_tomcat(tomcatApr):
        print("开始编译tomcat.........................................................")
        time.sleep(3)
        #tomcat
        replace("/tmp/tomcat/apr-1.6.5/configure","RM='$RM'","RM='$RM -f'")
        #make
        print("开始编译apr............................................................")
        time.sleep(3)
        checkApr = os.system("cd /tmp/tomcat/apr-* && ./configure --prefix=/usr/local/apr/ && make && make install")
        if 0 != checkApr:
            print("编译apr失败请检查相对应文件")
            os._exit(11)
        print("apr编译安装完成..........................................................")


        print("开始编译apr-iconv.......................................................")
        time.sleep(3)
        checkAprIconv = os.system("cd /tmp/tomcat/apr-iconv* && ./configure --prefix=/usr/local/apr-iconv/ "
                                  "--with-apr=/usr/local/apr && make && make install")
        if 0 != checkAprIconv:
            print("编译apr-iconv失败请检查相对应文件")
            os._exit(12)
        print("apr-iconv编译安装完成...................................................")


        print("开始编译expat..........................................................")
        time.sleep(3)
        checkExpat = os.system("cd /tmp/tomcat/expat* && ./configure --prefix=/usr/local/expat && make && make install ")
        if 0 != checkExpat:
            print("编译expat文件失败请检查依赖项")
            os._exit(13)
        print("expat编译安装完成......................................................")


        print("开始编译apr-util.......................................................")
        time.sleep(3)
        checkAprUtil = os.system("cd /tmp/tomcat/apr-util* && ./configure --prefix=/usr/local/apr-util"
                                 " --with-apr=/usr/local/apr --with-apr-iconv=/usr/local/apr-iconv/bin/apriconv"
                                 " --with-expat=/usr/local/expat && make && make install")
        if 0 != checkAprUtil:
            print("编译apr-util失败请检查相对应文件")
            os._exit(14)
        print("apr-util编译安装完成.......................................................")


        print("开始编译TomcatNative.......................................................")
        time.sleep(3)
        os.system("groupadd web && useradd -g web -s /bin/false -M tomcat")
        checkTomcatNative = os.system("cd /tmp/tomcat/apache-tomcat-*/bin/ && tar zxvf tomcat-native.tar.gz && "
                                      "cd tomcat-native-*/native && ./configure --with-apr=/usr/local/apr/bin/apr-1-config "
                                      "--with-java-home=" + jdkHome + " && make && make install")
        if 0 != checkTomcatNative:
            print("TomcatNative编译失败，请检查对应路径")
            os._exit(14)
        print("TomcatNative编译安装完成............................................................")

        print("安装 tomcat...................................................................")
        time.sleep(3)
        os.system("cp -R /usr/local/apr/lib/* /usr/lib64 && cp -R /usr/local/apr/lib/* /usr/lib")
        os.system("mv /tmp/tomcat/apache-tomcat* /usr/local/ && ln -s /usr/local/apache-tomcat* /usr/local/tomcat")
        os.system("ln -s /usr/local/tomcat/conf /etc/tomcat && ln -s /usr/local/tomcat/logs /var/log/tomcat")
        print("install tomcat done.................................................................")


def tomcat_optimization(tomcatApr):
    time.sleep(3)
    print("starting tomcat optimization......................................................")
    os.system("mv " + tomcatApr + "/server.xml /usr/local/tomcat/conf/")
    os.system("mv " + tomcatApr + "/tomcat-users.xml /usr/local/tomcat/conf/")
    tomcatProject = "/usr/local/tomcat/webapps/"
    os.system("mv " + tomcatApr + "/manager " + tomcatProject)
    os.system("chown -hR tomcat:web /usr/local/{apache-tomcat*,tomcat}")
    print("tomcat optimization done...........................................................")


def enable_tomcat(tomcatApr):

    os.system("cp /tmp/tomcat/tomcat-apr/tomcat /etc/init.d/tomcat && chmod 755 /etc/init.d/tomcat")
    os.system("chkconfig tomcat on")
    time.sleep(6)
    print("完成tomcat自启动...........................................................")


def system_firewalld():
    firewallPort= 'FW_SERVICES_EXT_TCP="8080 22"'
    os.system("service SuSEfirewall2_setup start")
    os.system("service SuSEfirewall2_init start")
    replace('/etc/sysconfig/SuSEfirewall2','FW_SERVICES_EXT_TCP=""',firewallPort)
    os.system("chkconfig SuSEfirewall2_setup on")
    os.system("chkconfig SuSEfirewall2_init on")
    os.system("service SuSEfirewall2_setup restart")
    os.system("service SuSEfirewall2_init restart")
    print("防火墙配置成功.................................................................")
    print("此服务器仅开放8080 22 端口,若需调整请联系系统维护人员..............................")



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

def install_tomcat():
    print("ss")

if __name__ == '__main__':
    system.tarz_tomcat()