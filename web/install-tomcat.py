# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-25
#version: 0.0.2

#centos 7.5
#在线安装需要将JDK解压到/usr/java 目录
#Offline installation dependency  tomcat apr apr-iconv apr-util
#use JDK1.7.0_80,CMS GC

import os
import time

def install_gcc():
    check = os.system("yum install -y gcc gcc-c++ libtool* autoconf automake expat-devel perl perl-devel wget")
    if 0 != check:
        print("请检查yum源是否正常使用")
        os._exit(3)


def download_tomcat():
    checkNetwork = os.system("ping mirror.bit.edu.cn -c 2")
    os.system("rm -rf /tmp/tomcat && mkdir -p /tmp/tomcat/download")
    if 0 == checkNetwork:
        os.system("wget -P /tmp/tomcat/download http://mirror.bit.edu.cn/apache/tomcat/tomcat-8/v8.5.34/bin/apache-tomcat-8.5.34.tar.gz")
        os.system("wget -P /tmp/tomcat/download http://mirror.bit.edu.cn/apache/apr/apr-1.6.5.tar.gz")
        os.system("wget -P /tmp/tomcat/download http://mirror.bit.edu.cn/apache/apr/apr-util-1.6.1.tar.gz")
        os.system("wget -P /tmp/tomcat/download http://mirror.bit.edu.cn/apache/apr/apr-iconv-1.2.2.tar.gz")
        os.system("for i in /tmp/tomcat/download/*.tar.gz;do tar zxvf $i -C /tmp/tomcat;done")
    if 0 !=checkNetwork:
        tomcatTarGz = raw_input("input tomcat tar.gz file path:")
        if not os.path.exists(tomcatTarGz):
            print("check path,path not exists")
            exit()
        tomcat = "/tmp/tomcat"
        os.system("tar zxvf " + tomcatTarGz + " -C " + tomcat)
        tomcatApr = tomcat+"/tomcat-apr"
        os.system("for i in " +tomcatApr+ "/*.tar.gz;do tar zxvf $i -C /tmp/tomcat/;done")
        os.system("mkdir /usr/java/")
        os.system("mv /tmp/tomcat/jdk* /usr/java/")
        return tomcatApr


def jdk_configure():
    #jdk
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


def make_tomcat(jdkHome):
    #tomcat
    defaultFileRead = open("/tmp/tomcat/apr-1.6.5/configure").readlines()
    updateFileWrite = open("/tmp/tomcat/apr-1.6.5/configure","r+")
    for defaultFile in defaultFileRead:
        updateFileWrite.write(defaultFile.replace("RM='$RM'","RM='$RM -f'"))
    updateFileWrite.close()
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
    print("开始编译apr-util.......................................................")
    time.sleep(3)
    checkAprUtil = os.system("cd /tmp/tomcat/apr-iconv* && ./configure --prefix=/usr/local/apr-util/ "
                             "--with-apr=/usr/local/apr --with-apr-iconv=/usr/local/apr-iconv/bin/apriconv "
                             "&& make && make install")
    if 0 != checkAprUtil:
        print("编译apr-util失败请检查相对应文件")
        os._exit(13)
    print("apr-util编译安装完成.......................................................")
    print("开始编译TomcatNative.......................................................")
    time.sleep(3)
    os.system("groupadd web && useradd -g web -s /bin/false tomcat")
    checkTomcatNative = os.system("cd /tmp/tomcat/apache-tomcat-*/bin/ && tar zxvf tomcat-native.tar.gz && "
                                  "cd tomcat-native-*/native && ./configure --with-apr=/usr/local/apr/bin/apr-1-config "
                                  "--with-java-home=" + jdkHome + " && make && make install")
    if 0 != checkTomcatNative:
        print("TomcatNative编译失败，请检查对应路径")
    print("TomcatNative编译安装完成............................................................")
    print("installing tomcat...................................................................")
    time.sleep(3)
    os.system("mv /tmp/tomcat/apache-tomcat* /usr/local/ && ln -s /usr/local/apache-tomcat* /usr/local/tomcat")
    os.system("cp -R /usr/local/apr/lib/* /usr/lib64 && cp -R /usr/local/apr/lib/* /usr/lib")
    print("install tomcat done.................................................................")


def tomcat_optimization(tomcatApr):
    time.sleep(3)
    print("starting tomcat optimization......................................................")
    os.system("mv -f " + tomcatApr +"/server.xml /usr/local/tomcat/conf/" )
    os.system("mv -f " + tomcatApr +"/tomcat-user.xml /usr/local/tomcat/conf/" )
    tomcatProject = "/usr/local/tomcat/webapps/project/"
    os.system("mkdir " + tomcatProject + " && mv " + tomcatApr + "/manager " + tomcatProject)
    os.system("chown -hR tomcat:web /usr/local/{apache-tomcat*,tomcat}")
    print("tomcat optimization done...........................................................")


def enable_tomcat(jdkHome):
    enableTomcat = open("/lib/systemd/system/tomcat.service","w")
    enableTomcat.write("[Unit]\n")
    enableTomcat.write("Description=Apache Tomcat 8\n")
    enableTomcat.write("After=syslog.target network.target\n\n")
    enableTomcat.write("[Service]\n")
    enableTomcat.write("Type=forking\n")
    enableTomcat.write("User=tomcat\n")
    enableTomcat.write("Group=web\n\n")
    enableTomcat.write("Environment=JAVA_HOME=" + jdkHome + "\n")
    enableTomcat.write("Environment=CATALINA_PID=/usr/local/tomcat/temp/tomcat.pid\n")
    enableTomcat.write("Environment=CATALINA_HOME=/usr/local/tomcat\n")
    enableTomcat.write("Environment=CATALINA_BASE=/usr/local/tomcat\n")
    enableTomcat.write("Environment='CATALINA_OPTS=-Dfile.encoding=UTF-8 -server -Xms4096m -Xmx4096m -Xmn1024m "
                       "-XX:MetaspaceSize=512M -XX:MaxMetaspaceSize=512M -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled "
                       "-XX:+HeapDumpOnOutOfMemoryError -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps "
                       "-Xloggc:/var/log/tomcat/gc.log -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly'\n")
    enableTomcat.write("Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'\n\n")
    enableTomcat.write("ExecStart=/usr/local/tomcat/bin/startup.sh\n")
    enableTomcat.write("ExecStop=/usr/local/tomcat/bin/shutdown.sh\n")
    enableTomcat.write("Restart=on-failure\n\n")
    enableTomcat.write("[Install]\n")
    enableTomcat.write("WantedBy=multi-user.target\n")
    enableTomcat.close()
    print("完成tomcat自启动...........................................................")
    print("test tomcat enable,.............................................")
    time.sleep(6)
    os.system("systemctl daemon-reload && systemctl enable tomcat && init 6")


def system_firewalld():
    os.system("systemctl start firewalld")
    os.system("firewall-cmd --permanent --add-port=8080/tcp --zone=public")
    os.system("firewall-cmd --permanent --add-service=ftp --zone=public")
    os.system("firewall-cmd --permanent --add-service=http --zone=public")
    os.system("firewall-cmd --reload")


def install_tomcat():
    install_gcc()
    tomcatApr = download_tomcat()
    jdkHome = jdk_configure()
    make_tomcat(jdkHome)
    #tomcat_optimization(tomcatApr)
    enable_tomcat(jdkHome)
    system_firewalld()

	
if __name__ == '__main__':
    print("此脚本运行环境为Centos7.5,若其他版本出现错误请自行更改或联系mail\n请使用root用户运行")
    time.sleep(5)
    install_tomcat()