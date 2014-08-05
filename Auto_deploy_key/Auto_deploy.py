#!/usr/local/python-2.7.3/bin/python
# -*- coding:utf8 -*-
#导入各模块
import getopt
import sys
from tasks import *
from config import app_dict
#----------------------------------------------------------------------------------------
def usage():
    print '''Help Information:
    -h/--help: Show help information
    -d: deploy app
    -r: rollback app
    --base 'cipm cx ...'
    --part1 'cm go2 ...'
    --part2 'cm2 carbiz2 ...'
    --part3 'cm3 carbiz3 ...'
    '''
#主函数
if __name__ == "__main__":
        try:
            opts,args=getopt.getopt(sys.argv[1:],'drh',['help','base=','part1=','part2=','part3='])
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
            elif o == '--part1':
                for p1 in a.split():
                    deploy_list.append(p1)
            elif o == '--part2':
                for p2 in a.split():
                    deploy_list.append(p2)
            elif o == '--part3':
                for p3 in a.split():
                    deploy_list.append(p3)
        if '-d' not in opts_list and '-r' not in opts_list:
            usage()
            sys.exit()
        if '-h' in opts_list or '--help' in opts_list:
            usage()
            sys.exit()

        username = raw_input("Input your username: ")
        password = raw_input("Input your password: ")

        if opts[0][0] == '-d':
            todo = Deploy()
            for apps in deploy_list:
                todo.connect(username, password,apps)
                todo.get_env(apps)
                todo.create_conf(apps)
                todo.unzip_file(apps)
                if app_dict[apps]["type"] == "app":
                    todo.app(apps)
                elif app_dict[apps]["type"] == "resin":
                    todo.resin(apps)
                else:
                    pass
                todo.finish()
        elif opts[0][0] == '-r':
            todo = Rollback()
            for apps in deploy_list:
                todo.connect(username, password,apps)
                if app_dict[apps]["type"] == "app":
                    todo.app(apps)
                elif app_dict[apps]["type"] == "resin":
                    todo.resin(apps)
                else:
                    pass
                todo.finish()
