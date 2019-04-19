# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/4/11


import configparser
import os
import shutil
import time

cf = configparser.ConfigParser()
confFilePath = "../test/fileOperating.conf"
cf.read(confFilePath,encoding="utf-8-sig")



def modeType():
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S")

    #configuration parameter
    modeType = cf.get("basic","modeType")
    oldDir = cf.get("basic","oldDir")
    newDir = cf.get("basic","newDir")
    logPath = cf.get("basic","logPath")

    #filter
    fileDate = cf.get("filter","fileDate")
    fileSuffix = cf.get("filter","fileSuffix")

    if "mv" in modeType:
        move(oldDir,newDir,logPath,fileDate,fileSuffix,nowTime)
    if 'cp' in modeType:
        copy(oldDir,newDir,logPath,fileDate,fileSuffix,nowTime)





def move(oldDir,newDir,logPath,fileDate,fileSuffix,nowTime):
    errorMessage = ""
    outPutFile = open(logPath,'w+')
    for root, dirs, files in os.walk(oldDir, topdown=False):
        fileNamePath = ""
        for name in files:
            if fileDate in name and fileSuffix in name:
                fileNamePath = (os.path.join(root,name))
            try:
                if fileNamePath:
                    shutil.move(fileNamePath,newDir)
            except shutil.Error as shutilError:
                errorMessage = str(shutilError)
            except BaseException as BaseError:
                errorMessage = str(BaseError)
            finally:
                outPutFile.write(errorMessage + "\n")

    outPutFile.write("完成时间"+nowTime)
    outPutFile.close()

def copy(oldDir,newDir,logPath,fileDate,fileSuffix,nowTime):
    errorMessage = ""
    outPutFile = open(logPath,'w+')
    for root, dirs, files in os.walk(oldDir, topdown=False):
        fileNamePath = ""
        for name in files:
            if fileDate in name and fileSuffix in name:
                fileNamePath = (os.path.join(root,name))
            try:
                if fileNamePath:
                    shutil.copy(fileNamePath,newDir)
            except shutil.Error as shutilError:
                errorMessage = str(shutilError)
            except BaseException as BaseError:
                errorMessage = str(BaseError)
            finally:
                outPutFile.write(errorMessage + "\n")

    outPutFile.write("完成时间"+nowTime)
    outPutFile.close()

if __name__ == '__main__':
    modeType()