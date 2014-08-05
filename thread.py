#!/usr/bin/python
from threading import Thread
import subprocess
from Queue import Queue
num_thread = 50
queue = Queue()
#ips = ["10.68.3.1","10.68.3.9","10.68.3.32","10.68.3.19","10.68.3.22","10.68.3.33"]

ips = map(lambda x:"10.68.3."+str(x),range(1,255)) 
def pinger(i,q):
    """ Pings subnet"""
    while True:
        ip = q.get()
        print "Thread %s: Pinging %s" % (i,ip)
        ret = subprocess.call("ping -c 1 %s" % ip,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT) 
        if ret == 0:
            print "%s: is alive" % ip
        else:
            print "%s did not respond" % ip
        q.task_done()

for i in range(num_thread):
    worker = Thread(target=pinger,args=(i,queue))
    worker.setDaemon(True)
    worker.start()

for ip in ips:
    queue.put(ip)
print "Main Thread Waiting"
queue.join()
print "Done"
