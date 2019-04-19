# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Poka
#Author: Duan Yu

import os
import shutil
import string
import configparser
cf = configparser.ConfigParser()
confFilePath = "../test/fileOperating.conf"
cf.read(confFilePath,encoding="utf-8-sig")

#移动文件 move file
a ="2312_20180401.FSN"
b ="2312_20190402.zip"
c ="2312_20190402.rar"
d =""

fileDateList = cf.get("filter","fileDate")
fileDateListSplit= str(fileDateList).split(",")
fileSuffix =""

print(string.rfind(a,fileDateListSplit) !=-1)