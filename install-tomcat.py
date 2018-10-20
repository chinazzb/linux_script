# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-18
#version: 0.0.2

##centos 7.5

import os
import time

def install_gcc():
    check = os.system("yum install -y gcc gcc-c++ libtool* autoconf automake expat-devel perl perl-devel")
    if 0 != check:
        print("请检查yum源是否正常使用")
        os._exit(3)

def install_tomcat():
    tarPath = raw_input("请输入tar.gz目录绝对路径:")
    print(tarPath)
    if os.path.exists(tarPath):
        #tar
        checkTar = os.system("for i in " +tarPath+"/*.tar.gz;do tar zxvf $i -C /tmp/;done")
        if 0 != checkTar:
            print("此路径下没有tar.gz文件，请检查路径")
            os._exit(4)
        #jdk
        os.system("mkdir /usr/java && mv /tmp/jdk* /usr/java/")
        profile = open("/etc/profile","a")
        profile.write("JAVA_HOME=/usr/java/jdk1.8.0_162\n")
        profile.write("JRE_HOME=$JAVA_HOME/jre\n")
        profile.write("CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib\n")
        profile.write("LD_LIBRARY_PATH=/usr/local/apr/lib:$LD_LIBRARY_PATH\n")
        profile.write("PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin\n")
        profile.write("export JAVA_HOME JRE_HOME PATH CLASSPATH LD_LIBRARY_PATH\n")


        #tomcat
        defaultFileRead = open("/tmp/apr-1.6.5/configure").readlines()
        updateFileWrite = open("/tmp/apr-1.6.5/configure","r+")
        for defaultFile in defaultFileRead:
            updateFileWrite.write(defaultFile.replace("RM='$RM'","RM='$RM -f'"))
        updateFileWrite.close()
        #make
        print("开始编译apr............................................................")
        time.sleep(3)
        checkApr = os.system("cd /tmp/apr-* && ./configure --prefix=/usr/local/apr/ && make && make install")
        if 0 != checkApr:
            print("编译apr失败请检查相对应文件")
            os._exit(11)
        print("apr编译安装完成..........................................................")
        print("开始编译apr-iconv.......................................................")
        time.sleep(3)
        checkAprIconv = os.system("cd /tmp/apr-iconv* && ./configure --prefix=/usr/local/apr-iconv/ "
                                  "--with-apr=/usr/local/apr && make && make install")
        if 0 != checkAprIconv:
            print("编译apr-iconv失败请检查相对应文件")
            os._exit(12)
        print("apr-iconv编译安装完成...................................................")
        print("开始编译apr-util.......................................................")
        time.sleep(3)
        checkAprUtil = os.system("cd /tmp/apr-iconv* && ./configure --prefix=/usr/local/apr-util/ "
                                 "--with-apr=/usr/local/apr --with-apr-iconv=/usr/local/apr-iconv/bin/apriconv "
                                 "&& make && make install")
        if 0 != checkAprUtil:
            print("编译apr-util失败请检查相对应文件")
            os._exit(13)
        print("apr-util编译安装完成.......................................................")
        print("开始编译TomcatNative.......................................................")
        time.sleep(3)
        os.system("groupadd web && useradd -g web -s /bin/false tomcat")
        jdkVersion = "jdk1.8.0_162"
        checkTomcatNative = os.system("cd /tmp/apache-tomcat-*/bin/ && tar zxvf tomcat-native.tar.gz && "
                                      "cd tomcat-native-*/native && ./configure --with-apr=/usr/local/apr/bin/apr-1-config "
                                      "--with-java-home=/usr/java/"+jdkVersion +"&& make && make install")
        if 0 != checkTomcatNative:
            print("TomcatNative编译失败，请检查对应路径")
        print("TomcatNative编译安装完成.......................................................")
        print("开始安装tomcat.................................................................")
        time.sleep(3)
        os.system("mv /tmp/apache-tomcat* /usr/local/ && ln -s /usr/local/apache-tomcat* /usr/local/tomcat && "
                  "chown -hR tomcat:tomcat /usr/local/{apache-tomcat*,tomcat}")
        os.system("cp -R /usr/local/apr/lib/* /usr/lib64 && cp -R /usr/local/apr/lib/* /usr/lib")
        print("安装tomcat完成.................................................................")

def enable_tomcat():
    enableTomcat = open("/lib/systemd/system/tomcat.service","w")
    enableTomcat.write("[Unit]\n")
    enableTomcat.write("Description=Apache Tomcat 8\n")
    enableTomcat.write("After=syslog.target network.target\n\n")
    enableTomcat.write("[Service]\n")
    enableTomcat.write("Type=forking\n")
    enableTomcat.write("User=tomcat\n")
    enableTomcat.write("Group=tomcat\n\n")
    enableTomcat.write("Environment=JAVA_HOME=/usr/java/jdk1.8.0_162\n")
    enableTomcat.write("Environment=CATALINA_PID=/usr/local/tomcat/temp/tomcat.pid\n")
    enableTomcat.write("Environment=CATALINA_HOME=/usr/local/tomcat\n")
    enableTomcat.write("Environment=CATALINA_BASE=/usr/local/tomcat\n")
    enableTomcat.write("Environment='CATALINA_OPTS=-Dfile.encoding=UTF-8 -server -Xms512m -Xmx512m -Xmn128m "
                       "-XX:SurvivorRatio=10 -XX:MaxTenuringThreshold=15 -XX:NewRatio=2 -XX:+DisableExplicitGC'\n")
    enableTomcat.write("Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'\n\n")
    enableTomcat.write("ExecStart=/usr/local/tomcat/bin/startup.sh\n")
    enableTomcat.write("ExecStop=/usr/local/tomcat/bin/shutdown.sh\n")
    enableTomcat.write("Restart=on-failure\n\n")
    enableTomcat.write("[Install]\n")
    enableTomcat.write("WantedBy=multi-user.target\n")
    enableTomcat.close()
    print("完成tomcat自启动...........................................................")
    print("测试tomcat自启动，即将重启服务器.............................................")
    time.sleep(6)
    os.system("systemctl daemon-reload && systemctl enable tomcat && init 6")


if __name__ == '__main__':
    print("此脚本运行环境为Centos7.5,若其他版本出现错误请自行更改或联系mail\n请使用root用户运行")
    time.sleep(5)
    install_gcc()
    install_tomcat()
    enable_tomcat()