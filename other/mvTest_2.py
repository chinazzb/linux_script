# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Poka
#Author: Duan Yu

import os
import shutil

#移动文件 move file
outPutFile = open("E:\\testDir\\move.log","w+")
errorMessage =""
try:
    shutil.move("E:\\testDir\\123.txt","E:\\back")
except shutil.Error as shutilError:
    errorMessage = str(shutilError)
except BaseException as allError:
    errorMessage = str(allError)
finally:
    outPutFile.write( errorMessage +"\n")
    outPutFile.close()