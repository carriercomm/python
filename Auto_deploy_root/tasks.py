# -*- coding:utf8 -*-
import os
import shutil
import time
from core import *
from config import *

#发布
class Deploy(object):
    def __init__(self):
        self.dotime = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))

    def create_conf(self,appname):
        app_temp_dir = template_path+appname
        app_conf_dir = deploy_dir+appname+"/conf"
        if not os.path.exists(app_conf_dir):
            os.makedirs(app_conf_dir)
        for filename in os.listdir(app_temp_dir):
            if filename == '81244006300012390.jks':
                shutil.copy2(app_temp_dir+'/'+filename, app_conf_dir+'/'+filename)
            else:
                genconfigfile(app_conf_dir+"/"+filename, app_temp_dir+"/"+filename, values_dict)

    def unzip_file(self,appname):
        app_data_dir = deploy_dir+appname+"/html"
        if appname == 'cm' or appname == 'cm2' or appname == 'cm3' or appname == 'cm4' or appname == 'cm5' or appname == 'cm6':
            app_soft_dir = softs_path+'cm'
        elif appname == 'go2' or appname == 'carbiz2' or appname == 'carbiz3' or appname == 'carbiz4' or appname == 'carbiz5' or appname == 'carbiz6':
            app_soft_dir = softs_path+'go2'
        elif appname == 'rb' or appname == 'rb2' or appname == 'rb3' or appname == 'rb4' or appname == 'rb5' or appname == 'rb6':
            app_soft_dir = softs_path+'rb'
        elif appname == 'order' or appname == 'order2' or appname == 'order3' or appname == 'order4' or appname == 'order5' or appname == 'order6':
            app_soft_dir = softs_path+'order'
        elif appname == 'radar' or appname == 'radar2' or appname == 'radar3' or appname == 'radar4' or appname == 'radar5' or appname == 'radar6':
            app_soft_dir = softs_path+'radar'
        elif appname == 'cx' or appname == 'cx2' or appname == 'cx3' or appname == 'cx4' or appname == 'cx5' or appname == 'cx6':
            app_soft_dir = softs_path+'cx'
        elif appname == 'engine' or appname == 'engine2' or appname == 'engine3' or appname == 'engine4' or appname == 'engine5' or appname == 'engine6':
            app_soft_dir = softs_path+'engine'
        elif appname == 'cipm' or appname == 'cipm2' or appname == 'cipm3' or appname == 'cipm4' or appname == 'cipm5' or appname == 'cipm6':
            app_soft_dir = softs_path+'cipm'
        elif appname == 'dataTransform' or appname == 'dataTransform2' or appname == 'dataTransform3' or appname == 'dataTransform4' or appname == 'dataTransform5' or appname == 'dataTransform6':
            app_soft_dir = softs_path+'dataTransform'
        elif appname == 'renewal' or appname == 'renewal2' or appname == 'renewal3' or appname == 'renewal4' or appname == 'renewal5' or appname == 'renewal6':
            app_soft_dir = softs_path+'renewal'
        elif appname == 'task-dispatcher' or appname == 'task-dispatcher2' or appname == 'task-dispatcher3' or appname == 'task-dispatcher4' or appname == 'task-dispatcher5' or appname == 'task-dispatcher6':
            app_soft_dir = softs_path+'task-dispatcher'
        else:
            app_soft_dir = softs_path+appname
        for s in os.listdir(app_soft_dir):
            cmds = "unzip -q -o %s -d %s" %(app_soft_dir+"/"+s,app_data_dir)
            os.system(cmds)

    def connect(self,username, password, appname): 
        connect(app_dict[appname]["ip"], port, username, password)
    
    def finish(self):
        finish()

    def get_env(self,appname):
        app_undo_file = rollback_dir+appname+"/undo"
        if not os.path.exists(rollback_dir+appname):
            os.makedirs(rollback_dir+appname)
        f = open(app_undo_file,'w')
        if app_dict[appname]["type"] == "resin":
            ls = "ls -l %s|grep '\->'|awk '{print $9,$11}'" % app_dict[appname]["dir"]
        else:
            #ls = "ls -l %s|grep '\->'|awk '{print $9,$11}'|grep %s" %(app_dict[appname]["dir"],appname)
            ls = "ls -l %s|grep '\->'|awk '{print $9,$11}'" % app_dict[appname]["dir"]
	cmds = []
        cmds.append(ls)
        ret = execute(cmds)
        for linkfile in ret[0][2]:
            #print linkfile.strip("\n")
            f.write(linkfile)
        f.close()
    def resin(self,appname):
        cmds = []
        stop = "/etc/init.d/resin stop"
        start = "/etc/init.d/resin start"
        if appname == 'dataTransform' or appname == 'dataTransform2' or appname == 'dataTransform3' or appname == 'dataTransform4' or appname == 'dataTransform5' or appname == 'dataTransform6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config"
        elif appname == 'cm' or appname == 'cm2' or appname == 'cm3' or appname == 'cm4' or appname == 'cm5' or appname == 'cm6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+'cm'
        elif appname == 'go2' or appname == 'carbiz2' or appname == 'carbiz3' or appname == 'carbiz4' or appname == 'carbiz5' or appname == 'carbiz6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+'go2'
        elif appname == 'rb' or appname == 'rb2' or appname == 'rb3' or appname == 'rb4' or appname == 'rb5' or appname == 'rb6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+'rb'
        elif appname == 'cx' or appname == 'cx2' or appname == 'cx3' or appname == 'cx4' or appname == 'cx5' or appname == 'cx6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+'cx'
        elif appname == 'engine' or appname == 'engine2' or appname == 'engine3' or appname == 'engine4' or appname == 'engine5' or appname == 'engine6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+'engine'
        elif appname == 'cipm' or appname == 'cipm2' or appname == 'cipm3' or appname == 'cipm4' or appname == 'cipm5' or appname == 'cipm6':
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+'cipm'
        else:
            conf_dir = "/data/www/ins_share"+self.dotime+"/config/"+appname
        data_dir = "/data/www/html"+self.dotime
        mkdir = "mkdir -p %s" % conf_dir
        rsync_conf = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
        rsync_data = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_html %s" %(rsync_server,appname,data_dir)
        chown = "chown -R www.www %s %s" %("/data/www/ins_share"+self.dotime,data_dir)
        rm_link = "rm -f /data/www/ins_share /data/www/html"
        build_conf_link = "ln -s %s %s" %("/data/www/"+"ins_share"+self.dotime,"/data/www/ins_share")
        build_data_link = "ln -s %s %s" %(data_dir,"/data/www/html")
        cmds.append(stop)
        cmds.append(mkdir)
        cmds.append(rsync_conf)
        cmds.append(rsync_data)
        cmds.append(chown)
        cmds.append(rm_link)
        cmds.append(build_conf_link)
        cmds.append(build_data_link)
        cmds.append(start)
        ret = execute(cmds)

    def app(self,appname):
        cmds = []
        stop = app_dict[appname]["stop"]
        start = app_dict[appname]["start"]
        if appname == 'order' or appname == 'order2' or appname == 'order3' or appname == 'order4' or appname == 'order5' or appname == 'order6':
            conf_dir = app_dict[appname]["dir"]+"order-service-server"+self.dotime+"/config/"
            data_dir = app_dict[appname]["dir"]+"order-service-server"+self.dotime
            rm_link = "rm -f /data/www/apps/order-service-server"
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"order-service-server")
            rsync_conf = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
            #chown = "chown -R www.www %s" % data_dir
        elif appname == 'renewal' or appname == 'renewal2' or appname == 'renewal3' or appname == 'renewal4' or appname == 'renewal5' or appname == 'renewal6':
            conf_dir = app_dict[appname]["dir"]+"renewal"+self.dotime
            data_dir = app_dict[appname]["dir"]+"renewal"+self.dotime
            rm_link = "rm -f %s" % app_dict[appname]["dir"]+"renewal"
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"renewal")
            rsync_conf = "rsync -aq --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
            #chown = "chown -R www.www %s" % data_dir
        elif appname == 'radar' or appname == 'radar2' or appname == 'radar3' or appname == 'radar4' or appname == 'radar5' or appname == 'radar6':
            conf_dir = app_dict[appname]["dir"]+"radar"+self.dotime+"/conf/env/com/"
            data_dir = app_dict[appname]["dir"]+"radar"+self.dotime
            rm_link = "rm -f %s" % app_dict[appname]["dir"]+"radar"
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"radar")
            rsync_conf = "echo nothing to do!" 
            #chown = "chown -R www.www %s" % data_dir
        elif appname == 'task-dispatcher' or appname == 'task-dispatcher2' or appname == 'task-dispatcher3' or appname == 'task-dispatcher4' or appname == 'task-dispatcher5' or appname == 'task-dispatcher6':
            conf_dir = app_dict[appname]["dir"]+"radar"+self.dotime+"/conf/env/com/"
            data_dir = app_dict[appname]["dir"]+"task-dispatcher"+self.dotime
            rm_link = "rm -f %s" % app_dict[appname]["dir"]+"task-dispatcher"
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"task-dispatcher")
            rsync_conf = "echo nothing to do!"
        #elif appname == 'radar2':
        #    conf_dir = app_dict[appname]["dir"]+"radar"+self.dotime+"/conf/env/com2/"
        #    data_dir = app_dict[appname]["dir"]+"radar"+self.dotime
        #    rm_link = "rm -f %s" % app_dict[appname]["dir"]+"radar"
        #    build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"radar")
        #    rsync_conf = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
        #    #chown = "chown -R www.www %s" % data_dir
        else:
            conf_dir = app_dict[appname]["dir"]+appname+self.dotime+"/config/"
            data_dir = app_dict[appname]["dir"]+appname+self.dotime
            rm_link = "rm -f %s" % app_dict[appname]["dir"]+appname
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+appname)
            rsync_conf = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
            #chown = "chown -R www.www %s" % data_dir
        chown = "chown -R www.www %s" % data_dir
        rsync_data = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_html %s" %(rsync_server,appname,data_dir)
        cmds.append(stop)
        cmds.append(rsync_data)
        cmds.append(rsync_conf) 
        cmds.append(chown)
        cmds.append(rm_link)
        cmds.append(build_link)
        cmds.append(start)
        ret = execute(cmds)

#回滚
class Rollback(object):
    def __init__(self):
        pass

    def connect(self,username, password, appname):
        connect(app_dict[appname]["ip"], port, username, password)

    def finish(self):
        finish()

    def resin(self,appname):
        f = open(rollback_dir+appname+'/'+'undo','r')
        for line in f:
            if line.split()[0] == 'html':
                 html = line.split()[1]
            elif line.split()[0] == 'ins_share':
                 ins_share = line.split()[1]
        f.close()
        cmds = []
        stop = "/etc/init.d/resin stop"
        start = "/etc/init.d/resin start"
        rm_link = "rm -f /data/www/ins_share /data/www/html"
        build_conf_link = "ln -s %s %s" %(ins_share,"/data/www/ins_share")
        build_data_link = "ln -s %s %s" %(html,"/data/www/html")
        cmds.append(stop)
        cmds.append(rm_link)
        cmds.append(build_conf_link)
        cmds.append(build_data_link)
        cmds.append(start)
        ret = execute(cmds)

    def app(self,appname):
        f = open(rollback_dir+appname+'/'+'undo','r')
        for line in f:
            dest_dir = app_dict[appname]["dir"]+line.split()[0]
            src_dir = line.split()[1]
        f.close()
        cmds = []
        stop = app_dict[appname]["stop"]
        start = app_dict[appname]["start"]
        rm_link = "rm -f %s" % dest_dir
        build_link = "ln -s %s %s" %(src_dir,dest_dir)
        cmds.append(stop)
        cmds.append(rm_link)
        cmds.append(build_link)
        cmds.append(start)
        ret = execute(cmds)
