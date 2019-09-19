#!/bin/bash
#Rotate the nginx logs to prevent
LOGS_PATH=/var/log/nginx/
CUR_LOGS_PATH=/usr/local/nginx/logs/
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
mv ${CUR_LOGS_PATH}/proxy_access.log $LOGS_PATH/proxy_access_${YESTERDAY}.log
mv ${CUR_LOGS_PATH}/error.log $LOGS_PATH/error_${YESTERDAY}.log
#
kill -USR1 $(cat /usr/local/nginx/logs/nginx.pid)

