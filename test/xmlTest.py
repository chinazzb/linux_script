# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#mail:chinazzbcn@gmail.com or cn-duanyu@foxmail.com
#Date: 2019/3/20
import xml.etree.ElementTree as ET
tree = ET.parse("../web/server.xml")
root = tree.getroot()

print root