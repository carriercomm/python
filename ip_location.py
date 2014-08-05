#!/usr/bin/env python
# -*- coding: utf-8 -*-
# the script is used to query the location of every ip
 
import urllib
import json
 
#淘宝ip库接口
url = "http://ip.taobao.com/service/getIpInfo.php?ip="
ip = "203.195.162.233"

data = urllib.urlopen(url + ip).read()
datadict=json.loads(data)
 
for oneinfo in datadict:
	#print oneinfo
        #print datadict[oneinfo]
        if "code" == oneinfo:
                #print oneinfo
                #print datadict[oneinfo]
               	if datadict[oneinfo] == 0:
        		print datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + "\t\t" + datadict["data"]["isp"]
