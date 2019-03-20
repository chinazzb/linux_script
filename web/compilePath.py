# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2018-10-25
#version: 0.0.2

#将源码装换成编译过的文件
import py_compile
import os

compilePathFile = raw_input("请输入需要转换文件的绝对路径:")

if not os.path.exists(compilePathFile):
    print("此路径不存在，请检查后再尝试!!!!!!!")
    os._exit(1)
py_compile.compile(compilePathFile)