# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-29
#version: 0.0.2


#centos 7.5


import os


def createUserGroup():
    os.system("groupadd -g 901 db2iadm1")
    os.system("groupadd -g 902 db2fadm1")
    os.system("groupadd -g 903 dasadm1")
    os.system("useradd -g db2iadm1 -u 801 -d /home/db2inst1 -m  db2inst1")
    os.system("useradd -g db2fadm1 -u 802 -d /home/db2fenc1 -m  db2fenc1")
    os.system("useradd -g dasadm1 -u 803 -d /home/dasadm1 -m  dasusr1")
    print("setting password to db2inst1 user")
    os.system("passwd db2inst1")

def db2Configure():
    os.system("cd /opt/ibm/db2/V9.7/instance")
    os.system("./dascrt -u dasusr1")
    os.system("./db2icrt -u db2inst1 db2inst1")
    os.system(".das/dasprofile")
    os.system("db2admin start")
