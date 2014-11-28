#!/usr/local/python-2.7.3/bin/python
# -*- coding:utf8 -*-
#导入各模块
import subprocess
import time
import getopt
import getpass
import sys
import os
from tasks import *
from config import app_dict
from multiprocessing import Process, Queue
#----------------------------------------------------------------------------------------
def usage():
    print '''Help Information:
    -h/--help: Show help information
    -d: deploy app
    -r: rollback app
    -c: check app
    --base 'auth ...'
    --part 'cm cm2 go2 ...'
    EXP :./Auto_deploy.py -d --base 'auth' --part 'cm cm2 go2'
    EXP1:./Auto_deploy.py -d --part 'zzb cipm cm cx go2 order radar rb task-dispatcher dataTransform messagePush engine renewal'
    EXP2:./Auto_deploy.py -d --part 'zzb2 cipm2 cm2 cx2 carbiz2 order2 radar2 rb2 task-dispatcher2 dataTransform2 messagePush2 engine2 renewal2'
    EXP3:./Auto_deploy.py -d --part 'zzb3 cipm3 cm3 cx3 carbiz3 order3 radar3 rb3 task-dispatcher3 dataTransform3 messagePush3 engine3 renewal3'
    EXP4:./Auto_deploy.py -d --part 'zzb4 cipm4 cm4 cx4 carbiz4 order4 radar4 rb4 task-dispatcher4 dataTransform4 messagePush4 engine4 renewal4'
    EXP5:./Auto_deploy.py -d --part 'zzb5 cipm5 cm5 cx5 carbiz5 order5 radar5 rb5 task-dispatcher5 dataTransform5 messagePush5 engine5 renewal5'
    EXP6:./Auto_deploy.py -d --part 'zzb6 cipm6 cm6 cx6 carbiz6 order6 radar6 rb6 task-dispatcher6 dataTransform6 messagePush6 engine6 renewal6'
    EXP7:./Auto_deploy.py -c --part 'cm cx go2 order rb dataTransform engine' 
    '''
#主函数
if __name__ == "__main__":
        try:
            opts,args=getopt.getopt(sys.argv[1:],'drch',['help','base=','part='])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        deploy_list = []
        opts_list = []
        for o,a in opts:
            opts_list.append(o)
            if o == '--base':
                for b in a.split():
                    deploy_list.append(b)
            elif o == '--part':
                for p in a.split():
                    deploy_list.append(p)
        if '-d' not in opts_list and '-r' not in opts_list and '-c' not in opts_list:
            usage()
            sys.exit()
        if '-h' in opts_list or '--help' in opts_list:
            usage()
            sys.exit()

        if opts[0][0] == '-c':
            todo = Check()
            for apps in deploy_list:
                print "Begine to check %s: %s." %(apps,todo.http_status(apps))
                #print todo.http_status(apps)
                #todo.http_status(apps)
            sys.exit()

        username = raw_input("Input your username: ")
        password = getpass.getpass("Input your password: ") 
        #password = raw_input("Input your password: ")
        q = Queue()
        for apps in deploy_list:
            q.put(apps)

        def do(i,q):
            while True:
                if q.empty():
                    sys.exit()
                apps = q.get()
                print "---------------------------------------------------------------------------"
                print "begin to deploy: %s" % apps
                print "pid:%s Process Number-%s: deploy %s" % (os.getpid(),i,apps)
                todo.connect(username, password,apps)
                todo.get_env(apps)
                todo.create_conf(apps)
                todo.rsync_file(apps)
                if app_dict[apps]["type"] == "app":
                    todo.app(apps)
                elif app_dict[apps]["type"] == "resin":
                    todo.resin(apps)
                elif app_dict[apps]["type"] == "tomcat":
                    todo.tomcat(apps)
                elif app_dict[apps]["type"] == "edi":
                    todo.edi(apps)
                else:
                    pass
                todo.finish()
                #time.sleep(20)

        def undo(i,q):
            while True:
                if q.empty():
                    sys.exit()
                apps = q.get()
                print "---------------------------------------------------------------------------"
                print "begin to rollback: %s" % apps
                print "pid:%s Process Number-%s: rollback %s" % (os.getpid(),i,apps)
                todo.connect(username, password,apps)
                if app_dict[apps]["type"] == "app":
                    todo.app(apps)
                elif app_dict[apps]["type"] == "resin":
                    todo.resin(apps)
                elif app_dict[apps]["type"] == "edi":
                    todo.edi(apps)
                else:
                    pass
                todo.finish()
                #time.sleep(20)
       
        print "Main process joins on queue"
        if opts[0][0] == '-d':
            todo = Deploy()
            for i in range(6):
                p = Process(target=do,args=[i,q])
                p.start()
                #time.sleep(1)
	elif opts[0][0] == '-r':
            todo = Rollback()
            for i in range(6):
                p = Process(target=undo,args=[i,q])
                p.start()
                #time.sleep(1)
#        elif opts[0][0] == '-c':
#            print deploy_list
        p.join()
        print "Main Program finished"
