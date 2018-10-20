# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-20
#version: 0.0.2


import os
import time

def download_software():
    if 0 != os.system("ping www.baidu.com -c 1"):
        print("check network DNS")
        os._exit(2)
    os.system("mkdir /tmp/nginx && cd /tmp/nginx && curl -O http://nginx.org/download/nginx-1.14.0.tar.gz && "
              "tar zxvf nginx-* -C /tmp/nginx")
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
    enableNginx.write("Type=forking\n")
    enableNginx.write("User=nginx\n")
    enableNginx.write("Group=web\n\n")
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
    print("完成nginx自启动...........................................................")
    print("测试nginx自启动，即将重启服务器.............................................")
    time.sleep(6)
    os.system("systemctl daemon-reload && systemctl enable nginx && init 6")
def install_nginx():
    install_gcc()
    download_software()
    print("starting configure nginx............................................")
    time.sleep(5)
    os.system("groupadd web && useradd -g web -s /bin/false nginx")
    if 0!= os.system("cd /tmp/nginx/nginx-* && ./configure --user=nginx --group=web --prefix=/usr/local/nginx --with-stream"):
        print("Configure nginx failed.........................................")
        os._exit(10)
    if 0!= os.system("cd /tmp/nginx/nginx* && make && make install"):
        print("make nginx failed ............................................")
    enable_nginx()

if __name__ == '__main__':
    install_nginx()
