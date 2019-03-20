# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/3/19

import os
import configparser

cf = configparser.ConfigParser()

cf.read("./install.conf",encoding="utf-8-sig")
# #获得所有大项
# secs = cf.sections()
# print(secs,type(secs))
# #获得db的参数
# opts = cf.options("db")
# print(opts)
# #获得db的参数的值
# kvs = cf.items("db")
# print(kvs,type(kvs))
test = cf.get("tomcat","tarFilePath")
print(test)


