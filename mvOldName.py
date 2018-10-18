# -*- coding: utf-8 -*-
#!/usr/bin/python
#python 3.6.5 and 2.6.8
#organization: China Shenzhen Poka
#Author: Duan Yu
#Mail:  cn-duanyu@foxmail.com or chinazzbcn@gmail.com

import shutil
import os

for root, dirs, files in os.walk('D:\\ftp', topdown=False):
    for name in files:
        filePath = (os.path.join(root,name))
        print (filePath)
        if shutil.

