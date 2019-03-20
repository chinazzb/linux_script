# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/3/20


import os

def depend():
    #six
    os.system("cd /tmp/python/six*/ && python setup.py install")

    #packaging
    os.system("cd /tmp/python/packaging*/ && python setup.py install")

    #pyparsing
    os.system("cd /tmp/python/pyparsing*/ && python setup.py install")

    #appdirs
    os.system("cd /tmp/python/appdirs*/ && python setup.py install")

    #setuptools
    os.system("cd /tmp/python/setuptools*/ && python setup.py install")

    #pip
    os.system("cd /tmp/python/pip*/ && python setup.py install")


def install_configparser():
    depend()




if __name__ == '__main__':
    install_configparser()