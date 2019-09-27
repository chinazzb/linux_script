#!/usr/bin/env bash
#install keepalived
set -e 
yum install -y gcc gcc-c++ openssl-devel libnl libnl-devel libnfnetlink-devel net-tools || zypper install -y  gcc gcc-c++ openssl libopenssl-devel
#work dir
workdir=`pwd`

#make
cd ./software/ && tar zxvf keepalived*.tar.gz -C /tmp/
cd /tmp/keepalived-* && ./configure --prefix=/usr/local/keepalived && make && make install

#configure file
cd $workdir
sudo mkdir /etc/keepalived && cp ./conf/keepalived/keepalived.conf /etc/keepalived/
cp ./conf/keepalived/keepalived.service /usr/lib/systemd/system/
sudo systemctl enable keepalived
cp ./conf/keepalived/http_check.sh /usr/local/bin/

#modify inetrface name and
#sed

#firewall configure
#systemctl start firewalld || syystemctl start SuSEfirewall2
#firewall-cmd --add-rich-rule='rule protocol value="vrrp" accept' --permanent || 
#firewall-cmd --reload


