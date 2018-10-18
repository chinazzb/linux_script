# -*- coding: utf-8 -*-
#!/usr/bin/python
#copyOrMoveFile.py

import os
import shutil
import xlrd
import string

#搜索文件函数
def search_file(path, filename):
    queue = []
    queue.append(path);
    while len(queue) > 0:
        tmp = queue.pop(0)
        #print(tmp)
        if(os.path.isdir(tmp)):#如果该路径是文件夹
            for item in os.listdir(tmp):#遍历该路径中文件和文件夹
                queue.append(os.path.join(tmp, item))#将所得路径加入队列queue
                #print(queue)
        elif(os.path.isfile(tmp)):#如果该路径是文件
            name = os.path.basename(tmp)#获取文件名
            #0400_0201_P04000400051T1_020100115A21801021347296.FSN
            #print(name)
            
            #文件目标存储目录： /fsn_cb_handin_1/2018/01/02/020100115A'
            
            year = '20' + name[36:38]
            #print(year)
            month = name[38:40]
            #print(month)
            day = name[40:42]
            #print(day)
            dotDataNumber = name[25:35]
            #print(dotDataNumber)
            
            #拼接路径
            path_list = ['fsn_cb_handin_1', year, month, day, dotDataNumber]
            newpath = ''
            for path in path_list:
                newpath = os.path.join(newpath, path)
            #print (newpath)
            
            #创建多层目录
            mkdirs(newpath)
            
            dirname = os.path.dirname(tmp)#获取文件目录
            full_path = os.path.join(dirname, name)#将文件名和文件目录连接起来，形成完整的路径
            #des_path = newpath + '/' + path + '_' + name #目标路径，将该文件信息添加进最后的文件名中
            des_path = newpath + '/' + name #目标路径，将该文件夹信息添加进最后的文件名中
            
            if filename in name: #匹配符合条件的文件，也可用if(name.find(filenmae)!=-1)
                #print(filename)
                shutil.copyfile(full_path,des_path)#复制文件到目标路径（复制+重命名）
                print('复制+重命名secssful!')
                #shutil.move(full_path, des_path)#移动文件到目标路径（移动+重命名）
                #print('移动+重命名成功')

                
###创建多层目录
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
        print(path + '创建成功')
        return True
    else:
        #如果目录存在则不创建，并提示目录已经存在
        print(path + '目录已经存在')
        return False
    


if __name__ == '__main__':
    
    dire = 'F:/TestDir/fsn_cb_handin/'
    name = '0400'
    
    #搜索文件
    search_file(dire,name.strip())
    
