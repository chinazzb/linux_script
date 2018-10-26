# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-25
#version: 0.0.2


#centos 7.5

import os
import time

def download_software():
    checkNetwork = os.system("ping www.taobao.com -c 2")
    os.system("rm -rf /tmp/nginx && mkdir -p /tmp/nginx")
    if 0 == checkNetwork:
        os.system("cd /tmp/nginx")
        os.system("for i in /tmp/nginx/*.tar.gz;do tar zxvf $i -C /tmp/nginx;done")
    if 0 !=checkNetwork:
        nginxTarDir = raw_input("input tomcat tar path:")
    if not os.path.exists(nginxTarDir):
        print("check path,path not exists")
        exit()
    os.system("for i in " +nginxTarDir+"/nginx*.tar.gz;do tar zxvf $i -C /tmp/nginx;done")
def install_gcc():
    if 0 != os.system("yum install -y pcre zlib pcre-devel zlib-devel gcc gcc-c++"):
        print("check yum repo.d .................................................")
        os._exit(2)
def enable_nginx():
    enableNginx = open("/lib/systemd/system/nginx.service","w")
    enableNginx.write("[Unit]\n")
    enableNginx.write("Description=nginx 1.14.0\n")
    enableNginx.write("After=network.target remote-fs.target nss-lookup.target\n\n")
    enableNginx.write("[Service]\n")
    enableNginx.write("Type=forking\n\n")
    enableNginx.write("PIDFile=/usr/local/nginx/logs/nginx.pid\n")
    enableNginx.write("ExecStartPre=/usr/bin/rm -f //usr/local/nginx/logs/nginx.pid\n")
    enableNginx.write("ExecStartPre=/usr/local/nginx/sbin/nginx -t\n")
    enableNginx.write("ExecStart=/usr/local/nginx/sbin/nginx\n")
    enableNginx.write("ExecReload=/bin/kill -s HUP $MAINPID\n")
    enableNginx.write("KillSignal=SIGQUIT\n")
    enableNginx.write("TimeoutStopSec=5\n")
    enableNginx.write("KillMode=process\n")
    enableNginx.write("PrivateTmp=true\n\n")
    enableNginx.write("[Install]\n")
    enableNginx.write("WantedBy=multi-user.target\n")
    enableNginx.close()
    if  0 == os.system("systemctl daemon-reload && systemctl enable nginx"):
        print("完成nginx自启动...........................................................")
    print("测试nginx自启动，即将重启服务器.............................................")
    time.sleep(6)
    os.system("init 6")

def make_nginx():
    print("starting configure nginx............................................")
    time.sleep(5)
    os.system("groupadd web && useradd -g web -s /bin/false nginx")
    if 0!= os.system("cd /tmp/nginx/nginx-* && ./configure --user=nginx --group=web --prefix=/usr/local/nginx --with-stream"):
        print("Configure nginx failed.........................................")
        os._exit(10)
    if 0!= os.system("cd /tmp/nginx/nginx* && make && make install"):
        print("make nginx failed ............................................")
def install_nginx():
    install_gcc()
    download_software()
    make_nginx()
    enable_nginx()

if __name__ == '__main__':
    print("此脚本运行环境为Centos7.5,若其他版本出现错误请自行更改或联系mail\n请使用root用户运行")
    time.sleep(5)
    install_nginx()
