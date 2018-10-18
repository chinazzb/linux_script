# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Shenzhen Poka
#Author: Duan Yu
#Mail:  cn-duanyu@foxmail.com or chinazzbcn@gmail.com
import os
def scanfile(path):
    oneList = []
    twoList = []
    #第一层
    dirList = os.listdir(path)
    for dirName in dirList:
        dirPath = os.path.join(path,dirName)
        if os.path.isdir(dirPath):
            oneList.append(dirPath)
    #第二层
    for dirTwoList in oneList:
        print(len(dirTwoList))
        if len(dirTwoList) == 29:
            dirTwoList2 = os.listdir(dirTwoList)
            for dirTwoName in dirTwoList2:
                dirTwoPath = os.path.join(dirTwoList,dirTwoName)
                if os.path.isdir(dirTwoPath):
                    twoList.append(dirTwoPath)
    #print(twoList)
    #删除
    for twoPath in twoList:
        print('rm -rf '+twoPath+'/201801*')
        # os.system('rm -rf '+twoPath+'/201801*')
        # os.system('rm -rf '+twoPath+'/201802*')
        # os.system('rm -rf '+twoPath+'/201803*')
        # os.system('rm -rf '+twoPath+'/201804*')
        # os.system('rm -rf '+twoPath+'/201805*')




if __name__ == '__main__':
    scanfile('/home/poka/fsn_cb_handin')
