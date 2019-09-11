#!/usr/bin/env bash
# install keepalived

yum install gcc gcc-c++ openssl-devel libnl libnl-devel libnfnetlink-devel net-tools -y

#make
cd ./software/ && tar xvf keepalived.tar -C /tmp/
cd /tmp/keepalived/ && tar zxvf keepalived-*.tar.gz
cd keepalived-* && ./configure --prefix=/usr/local/keepalived && make && make install

#configure file
sudo mkdir /etc/keepalived && cp /tmp/keepalived/keepalived.conf /etc/keepalived/
cp /tmp/keepalived/keepalived.service /usr/lib/systemd/system/
sudo systemctl enable keepalived
cp /tmp/keepalived/nginx_check.sh /usr/local/bin/

