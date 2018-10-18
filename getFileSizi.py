# -*- coding: utf-8 -*-
#!/usr/bin/python
#python version: 3.6.5 and 2.6.8
#organization: China Poka
#Author: Duan Yu

import os
import time
import datetime
import shutil

#转换成KB或者MB
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)
#获得文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)

#
def get_file(oldPath):
    #日志
    outputFile = open("H:\\getFilePath.log",'w+')
    for root, dirs, files in os.walk(oldPath, topdown=False):
        for name in files:
            pathName = (os.path.join(root,name))
            fileSize = getDocSize(pathName)
            outputFile.write(pathName+" "+fileSize+"\n")
    outputFile.close()
#main idea
if __name__ == '__main__':
    get_file("H:\\LangFangData\\fsnBack\\fsn_cb_handin")
    #move_file("H:\LangFangData\fsnBack\fsn_cb_handin\0202")