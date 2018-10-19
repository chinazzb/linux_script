# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-18
#version: 0.0.2


import os
def install_gcc():
    if 0 != os.system("yum install -y pcre zlib gcc gcc-c++"):
        print()

