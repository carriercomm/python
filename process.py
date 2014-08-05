#!/usr/bin/python
from multiprocessing import Process, Queue,Pool
import time
import subprocess
from IPy import IP
import sys,os

q = Queue()
ips = IP("10.68.3.0/24")
def f(i,q):
    while True:
        if q.empty():
            sys.exit()
        #print "Process Number: %s" % i
        ip = q.get()
        ret = subprocess.call("ping -c 1 %s" % ip, shell=True, stdout=open('/dev/null'), stderr=subprocess.STDOUT)
        if ret == 0:
            #pass
            print "pid:%s Process Number-%s: %s: is alive" % (os.getpid(),i,ip)
        else:
            print "pid:%s Process Number-%s: didn't find a response for %s" % (os.getpid(),i,ip)
for ip in ips:
    q.put(ip)

for i in range(8):
    p = Process(target=f,args=[i,q])
    p.start()

print "Main process joins on queue"
p.join()
print "Main Program finished"
