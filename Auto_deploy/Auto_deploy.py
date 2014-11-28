#!/usr/local/python-2.7.3/bin/python
# -*- coding:utf8 -*-
#导入各模块
import getopt
import getpass
import sys
from tasks import *
from config import app_dict
#----------------------------------------------------------------------------------------
def usage():
    print '''Help Information:
    -h/--help: Show help information
    -d: deploy app
    -r: rollback app
    --base 'auth ...'
    --part 'cm cm2 go2 ...'
    EXP :./Auto_deploy.py -d --base 'auth' --part 'cm cm2 go2'
    EXP1:./Auto_deploy.py -d --part 'cipm cm cx go2 order radar rb task-dispatcher dataTransform engine renewal'
    EXP2:./Auto_deploy.py -d --part 'cipm2 cm2 cx2 carbiz2 order2 radar2 rb2 task-dispatcher2 dataTransform2 engine2 renewal2'
    EXP3:./Auto_deploy.py -d --part 'cipm3 cm3 cx3 carbiz3 order3 radar3 rb3 task-dispatcher3 dataTransform3 engine3 renewal3'
    EXP4:./Auto_deploy.py -d --part 'cipm4 cm4 cx4 carbiz4 order4 radar4 rb4 task-dispatcher4 dataTransform4 engine4 renewal4'
    EXP5:./Auto_deploy.py -d --part 'cipm5 cm5 cx5 carbiz5 order5 radar5 rb5 task-dispatcher5 dataTransform5 engine5 renewal5'
    EXP6:./Auto_deploy.py -d --part 'cipm6 cm6 cx6 carbiz6 order6 radar6 rb6 task-dispatcher6 dataTransform6 engine6 renewal6'
    '''
#主函数
if __name__ == "__main__":
        try:
            opts,args=getopt.getopt(sys.argv[1:],'drh',['help','base=','part='])
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
        if '-d' not in opts_list and '-r' not in opts_list:
            usage()
            sys.exit()
        if '-h' in opts_list or '--help' in opts_list:
            usage()
            sys.exit()

        username = raw_input("Input your username: ")
        password = getpass.getpass("Input your password: ") 
        #password = raw_input("Input your password: ")

        if opts[0][0] == '-d':
            todo = Deploy()
            #print deploy_list
            for apps in deploy_list:
                print "---------------------------------------------------------------------------"
                print "begin to deploy: %s" % apps
                todo.connect(username, password,apps)
                todo.get_env(apps)
                todo.create_conf(apps)
                #todo.unzip_file(apps)
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
        elif opts[0][0] == '-r':
            todo = Rollback()
            for apps in deploy_list:
                print "---------------------------------------------------------------------------"
                print "begin to rollback: %s" % apps
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
