#!/usr/bin/env bash
#modify projec name 

#default 
oldProject=evaluate
newProject=evaluate_test

#tomcat rename
echo "configuring tomcat project name..............."

service tomcat stop
mv /usr/local/tomcat/webapps/$oldProject /usr/local/tomcat/webapps/$newProject
service tomcat start

echo "tomcat project done...................."
echo -e "\t\t\n\t\t"


#nginx rename
echo "configuring nginx configuration file ..................."

sed -i "s#$oldProject#$newProject#" /etc/nginx/nginx.conf
service nginx reload

echo "nginx configuration file done ........................"
