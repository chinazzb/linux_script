# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Shenzhen Poka
#Author: Duan Yu

import os
import shutil

#create new path	创建新路径
def mkdirs(path):
    #去除首位空格
    path = path.strip()
    #去除尾部\符号
    path = path.rstrip("\\")

    #判断路径是否存在
    #存在 True
    #不存在False
    isExists = os.path.exists(path)

    #判断结果
    if not isExists:
        #创建目录操作函数
        os.makedirs(path)
        #如果不存在则创建目录
        #print(path + '创建成功')
        return True
    else:
        #如果目录存在则不创建，并提示目录已经存在
        #print(path + '目录已经存在')
        return False

#get new path	获得新路径
def getFileDataBank(fileName,startIndex,endIndex):
    fileBankData = []
    bankNumber = fileName[5:9]
    fileGenerate = fileName[startIndex:endIndex]
    fileGenerate = "20" + fileGenerate
    fileBankData.append(fileGenerate)
    fileBankData.append(bankNumber)
    newPath = ""
    pathList = ["H:\\fsnFiles",fileBankData[0],fileBankData[1]]
    for path in pathList:
        newPath = os.path.join(newPath,path)
    return newPath


#根据文件判断网点、文件生成日期
def arrange_dir(fileName):
    #lenght 长度 53 or 46
    pathLength = len(fileName)

    #fsn file
    if ".FSN" in fileName:
        #清分机文件
        if pathLength == 53:
            newPath = getFileDataBank(fileName,36,42)
            return newPath
        #点钞机文件
        if pathLength == 46:
            newPath = getFileDataBank(fileName,25,34)
            return newPath
        #蓝标文件、ATM文件
        if pathLength == 92:
            newPath = getFileDataBank(fileName,66,75)
            return newPath
    if ".SK" in fileName:

#move file,error message write log  移动文件,错误信息写入文件 
def move_file(oldPath,logPath):
    #error message
    errorMessage = ""
    #open log file
    outPutFile = open(logPath,"w+")
    for root, dirs, files in os.walk(oldPath, topdown=False):
        for name in files:
            fileName = name
            filePath = (os.path.join(root,name))
            newPath = arrange_dir(fileName)
            # try:
            #     mkdirs(newPath)
            #     shutil.move(filePath,newPath)
            # except shutil.Error as shutilError:
            #     errorMessage = str(shutilError)
            # except BaseException as BaseError:
            #     errorMessage = str(BaseError)
            # finally:
            #     outPutFile.write(errorMessage + "\n")

    outPutFile.close()


#main idea
if __name__ == '__main__':
    #need arrange dir
    oldPath = "H:\\rh\\home\\poka\\fsn_cb_handin\\0201bak\\0201\\20180110\\020100125A\\020100125A21801101354589"

	#log save path
    logPath = "H:\\move-fsn-cb-handin.log"
    #
    move_file(oldPath,logPath)
