#!/usr/bin/env bash
# install keepalived

set -e

yum install gcc gcc-c++ openssl-devel libnl libnl-devel libnfnetlink-devel net-tools -y

#make
cd ./software/ && tar zxvf keepalived*.tar -C /tmp/
cd /tmp/keepalived-* && ./configure --prefix=/usr/local/keepalived && make && make install

#configure file
sudo mkdir /etc/keepalived && cp ./conf/keepalived/keepalived.conf /etc/keepalived/
cp ./conf/keepalived/keepalived.service /usr/lib/systemd/system/
sudo systemctl enable keepalived
cp ./conf/keepalived/http_check.sh /usr/local/bin/

#firewall configure

systemctl start firewalld
firewall-cmd --add-rich-rule='rule protocol value="vrrp" accept' --permanent
firewall-cmd --reload
