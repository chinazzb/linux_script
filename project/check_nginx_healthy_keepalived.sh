#!/usr/bin/env bash
#keepalived + nginx 
#auto switching

URL="127.0.0.1/chk_nginx.html"
#if nginx healthy then snatch back VIP 

PID_FILE=/var/run/keepalived.pid
/usr/bin/curl --connect-timeout 20 $URL > /dev/null 2>&1
if [ ! -f $PID_FILE -a $? -eq 0  ];then
    echo `date` ':nginx is healthy, try to keepalived' >> /var/log/keepalived
    /usr/bin/systemctl start keepalived
    exit
fi

#if nginx not healthy then kill keepalived switching VIP
PID=`cat /var/run/keepalived.pid`
/usr/bin/curl --connect-timeout 20 $URL > /dev/null 2>&1
if [  $? -ne 0 ];then
    echo `date` ': nginx is not healthy, try to killall keepalived ' >> /var/log/keepalived
    /usr/bin/kill -TERM $PID && echo `date` ': keepalived killed ' >> /var/log/keepalived
fi