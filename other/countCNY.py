# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#Date:
#version:


import os
import re

count = 0
for root,dirs,files in os.walk("C:\\Users\\DuanYU\\Desktop\\temp",topdown=False):
    for name in files:
        suffixName = re.compile(".pdf")
        sum = suffixName.sub("0",name)
        count = count + float(sum)
print(count)