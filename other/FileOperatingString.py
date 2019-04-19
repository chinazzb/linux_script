# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/4/16



import os
import shutil
import time


def modeType():
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S")

    #configuration parameter
    modeType =
    oldDir =
    newDir =
    logPath =

    #filter
    fileDate =
    fileSuffix =

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