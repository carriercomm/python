#!/usr/bin/env python
#coding=utf-8
"""
 @desc: 主要就是用于通过ip138的url 获取ip地址的归属地
 @date 2013-09-26
"""
import sys
import re
import os
import time
import urllib2

class ip138:
    '处理关于url获取后的一些字符查找替换工作'

    def __init__(self,ip):
        self.ip = ip

    def __open(self):
        return urllib2.urlopen('http://ip138.com/ips138.asp?ip='+self.ip + '&action=2')
    def __recompile(self):
        return re.compile(r'.*<li>(.*)</li><li>(.*)</li>.*')
    def get(self):
        p = self.__recompile()
        lines = self.__open()
        for line in lines :
            if '<ul class="ul1">'  in line:
                return p.sub(r'\1\n',line).decode('gbk')

os.system("netstat -an |grep ESTAB |awk {'print $5'} |awk -F : {'print $1'}|sed '/^$/d'|sed '/^127.0/d' |sort|uniq -c|sort -rn|awk {'print $1,$2'}>iplist.txt")

f = open("iplist.txt")

for line in f:
        a = line.split()
        #print a[0]
	#line = line.strip('\n')
        #print line
	m=ip138(a[1])
        print "查询的ip: %s 连接数: %s\n%s" %(a[1],a[0],m.get().encode('utf-8')),
	time.sleep(1) 

f.close()
