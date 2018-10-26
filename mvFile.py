# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Poka
#Author: Duan Yu

import os
import shutil


#寻找最终目录下的文件  find finally dir inside files
def move_file(oldPath,newPath):
    errorMessage = ""
    outPutFile = open("mvFile.log",'w+')
    for root, dirs, files in os.walk(oldPath, topdown=False):
        for name in files:
            pathName = (os.path.join(root,name))
            outPutFile.write(pathName + "\n")
            try:
                shutil.move(pathName,newPath)
            except shutil.Error as shutilError:
                errorMessage = str(shutilError)
            except BaseException as BaseError:
                errorMessage = str(BaseError)
            finally:
                outPutFile.write(errorMessage + "\n")
    outPutFile.close()
#main ideas
if __name__ == '__main__':
    #fsn文件路径(只需要一个主目录即可)
    oldPath = "F:\TestDir\evaluate-tables"
    newPath = "E:\\fileDir"
    move_file(oldPath,newPath)
