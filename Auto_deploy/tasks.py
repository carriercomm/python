# -*- coding:utf8 -*-
import os
import shutil
import time
import requests
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
        elif appname == 'messagePush' or appname == 'messagePush2' or appname == 'messagePush3' or appname == 'messagePush4' or appname == 'messagePush5' or appname == 'messagePush6':
            app_soft_dir = softs_path+'messagePush'
        elif appname == 'renewal' or appname == 'renewal2' or appname == 'renewal3' or appname == 'renewal4' or appname == 'renewal5' or appname == 'renewal6':
            app_soft_dir = softs_path+'renewal'
        elif appname == 'task-dispatcher' or appname == 'task-dispatcher2' or appname == 'task-dispatcher3' or appname == 'task-dispatcher4' or appname == 'task-dispatcher5' or appname == 'task-dispatcher6':
            app_soft_dir = softs_path+'task-dispatcher'
        else:
            app_soft_dir = softs_path+appname
        for s in os.listdir(app_soft_dir):
            cmds = "unzip -q -o %s -d %s" %(app_soft_dir+"/"+s,app_data_dir)
            os.system(cmds)

    def rsync_file(self,appname):
        app_data_dir = deploy_dir+appname+"/html"
        if appname in ('renbao','renbao2','renbao3','renbao4','renbao5','renbao6'):
            app_soft_dir = softs_path+"renbao"
        elif appname in ('guoshoucai' 'guoshoucai2' 'guoshoucai3' 'guoshoucai4' 'guoshoucai5' 'guoshoucai6'):
            app_soft_dir = softs_path+"guoshoucai"
        elif appname in ('zzb','zzb1','zzb2','zzb3','zzb4','zzb5','zzb6'):
	    app_soft_dir = softs_path+"zzb"
        elif appname == 'cm' or appname == 'cm2' or appname == 'cm3' or appname == 'cm4' or appname == 'cm5' or appname == 'cm6':
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
        elif appname == 'messagePush' or appname == 'messagePush2' or appname == 'messagePush3' or appname == 'messagePush4' or appname == 'messagePush5' or appname == 'messagePush6':
            app_soft_dir = softs_path+'messagePush'
        elif appname == 'renewal' or appname == 'renewal2' or appname == 'renewal3' or appname == 'renewal4' or appname == 'renewal5' or appname == 'renewal6':
            app_soft_dir = softs_path+'renewal'
        elif appname == 'task-dispatcher' or appname == 'task-dispatcher2' or appname == 'task-dispatcher3' or appname == 'task-dispatcher4' or appname == 'task-dispatcher5' or appname == 'task-dispatcher6':
            app_soft_dir = softs_path+'task-dispatcher'
        else:
            app_soft_dir = softs_path+appname
        cmds = "rsync -a --delete %s %s" %(app_soft_dir+"/",app_data_dir)
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

    def tomcat(self,appname):
        cmds = []
        stop = "/etc/init.d/tomcat stop"
        start = "/etc/init.d/tomcat start"
        if appname in ('zzb' 'zzb1' 'zzb2' 'zzb3' 'zzb4' 'zzb5' 'zzb6'):
            #conf_dir = app_dict[appname]["dir"]+"html"+self.dotime+"/WEB-INF/classes/"
            cmd1 = "rsync -a --delete %s %s" %(template_path+appname+"/jdbc.dicon",deploy_dir+appname+"/html/WEB-INF/classes/")
            cmd2 = "rsync -a --delete %s %s" %(template_path+appname+"/jdbc.properties",deploy_dir+appname+"/html/WEB-INF/classes/")
            cmd3 = "rsync -a --delete %s %s" %(template_path+appname+"/common.js",deploy_dir+appname+"/html/ZZBWeb/Buy/")
            os.system(cmd1)
            os.system(cmd2)
            os.system(cmd3)
            rsync_conf = "echo no zzb confiugure file for rsync!"
            build_conf_link = "echo no zzb confiugure file for link"
            data_dir = "/data/www/html"+self.dotime
            rsync_data = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_html %s" %(rsync_server,appname,data_dir)
            rm_link = "rm -f /data/www/html"
            build_data_link = "ln -s %s %s" %(data_dir,"/data/www/html")
        chown = "chown -R www.www %s"  %data_dir
        cmds.append(stop)
        cmds.append(rsync_conf)
        cmds.append(rsync_data)
        cmds.append(chown)
        cmds.append(rm_link)
        cmds.append(build_conf_link)
        cmds.append(build_data_link)
        cmds.append(start)
        ret = execute(cmds)

    def edi(self,appname):
        cmds = []
        stop = "/etc/init.d/tomcat stop"
        start = "/etc/init.d/tomcat start"
        cmd1 = "rsync -a --delete %s %s" %(template_path+appname+"/EdiConfig.gdsl",deploy_dir+appname+"/html/WEB-INF/classes/subSystemConfig/")
        cmd2 = "rsync -a --delete %s %s" %(template_path+appname+"/messageSync.config",deploy_dir+appname+"/html/WEB-INF/classes/subSystemConfig/")
        cmd3 = "rsync -a --delete %s %s" %(template_path+appname+"/init.properties",deploy_dir+appname+"/html/WEB-INF/classes/subSystemConfig/")
        cmd4 = "rsync -a --delete %s %s" %(template_path+appname+"/remoteconfigure.xml",deploy_dir+appname+"/html/WEB-INF/classes/subSystemConfig/jira/")
        cmd5 = "rsync -a --delete %s %s" %(template_path+appname+"/iceStorm.config",deploy_dir+appname+"/html/WEB-INF/classes/subSystemConfig/jira/")
        cmd6 = "rsync -a --delete %s %s" %(template_path+appname+"/ehcache-task.xml",deploy_dir+appname+"/html/WEB-INF/classes/subSystemConfig/cache/")
        cmd7 = "rsync -a --delete %s %s" %(template_path+appname+"/applicationContext-akkaServer.xml",deploy_dir+appname+"/html/WEB-INF/classes/systemConfig/")
        os.system(cmd1)
        os.system(cmd2)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd5)
        os.system(cmd6)
        os.system(cmd7)

        if appname in ('renbao' 'renbao2' 'renbao3' 'renbao4' 'renbao5' 'renbao6'):
            edipath = "/data/www/edi/renbao"
            data_dir = "/data/www/edi/renbao"+self.dotime
        if appname in ('guoshoucai' 'guoshoucai2' 'guoshoucai3' 'guoshoucai4' 'guoshoucai5' 'guoshoucai6'):
            edipath = "/data/www/edi/guoshoucai"
            data_dir = "/data/www/edi/guoshoucai"+self.dotime
        rm_link = "rm -f %s" %edipath
        build_data_link = "ln -s %s %s" %(data_dir,edipath)
        rsync_data = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_html %s" %(rsync_server,appname,data_dir)
        chown = "chown -R www.www %s"  %data_dir
        #cmds.append(stop)
        cmds.append(rsync_data)
        cmds.append(chown)
        #cmds.append(rm_link)
        #cmds.append(build_data_link)
        #cmds.append(start)
        ret = execute(cmds)

    def app(self,appname):
        cmds = []
        stop = app_dict[appname]["stop"]
        start = app_dict[appname]["start"]
        #if appname == 'order' or appname == 'order2' or appname == 'order3' or appname == 'order4' or appname == 'order5' or appname == 'order6':
        if appname in ('order','order2','order3','order4','order5','order6'):
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
            rsync_conf = "echo no radar confiugure file for rsync!" 
            #chown = "chown -R www.www %s" % data_dir
        elif appname in ('task-dispatcher','task-dispatcher2','task-dispatcher3','task-dispatcher4','task-dispatcher5','task-dispatcher6'):
            conf_dir = app_dict[appname]["dir"]+"radar"+self.dotime+"/conf/env/com/"
            data_dir = app_dict[appname]["dir"]+"task-dispatcher"+self.dotime
            rm_link = "rm -f %s" % app_dict[appname]["dir"]+"task-dispatcher"
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"task-dispatcher")
            rsync_conf = "echo no task-dispatcher confiugure file for rsync!"
        #elif appname == 'radar2':
        #    conf_dir = app_dict[appname]["dir"]+"radar"+self.dotime+"/conf/env/com2/"
        #    data_dir = app_dict[appname]["dir"]+"radar"+self.dotime
        #    rm_link = "rm -f %s" % app_dict[appname]["dir"]+"radar"
        #    build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"radar")
        #    rsync_conf = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
        #    #chown = "chown -R www.www %s" % data_dir
        elif appname in ('messagePush','messagePush2','messagePush3','messagePush4','messagePush5','messagePush6'):
            conf_dir = app_dict[appname]["dir"]+"messagePush"+self.dotime+"/res/"
            data_dir = app_dict[appname]["dir"]+"messagePush"+self.dotime
            rm_link = "rm -f /data/www/apps/messagePush"
            build_link = "ln -s %s %s" %(data_dir,app_dict[appname]["dir"]+"messagePush")
            rsync_conf = "rsync -aq --delete --password-file=/etc/rsync_passwd test@%s::%s_conf %s" %(rsync_server,appname,conf_dir)
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

    def edi(self,appname):
        f = open(rollback_dir+appname+'/'+'undo','r')
        keyword = filter(str.isalpha, appname)
        for line in f:
            if line.find(keyword) > -1:
                dest_dir = app_dict[appname]["dir"]+line.split()[0]
                src_dir = line.split()[1]
        f.close()
        cmds = []
        #stop = app_dict[appname]["stop"]
        #start = app_dict[appname]["start"]
        rm_link = "rm -f %s" % dest_dir
        build_link = "ln -s %s %s" %(src_dir,dest_dir)
        #cmds.append(stop)
        #cmds.append(rm_link)
        #cmds.append(build_link)
        #cmds.append(start)
        ret = execute(cmds)

##检测
class Check(object):
    def __init__(self):
        pass

    def http_status(self,appname):
        keyword = filter(str.isalpha, appname)
        if keyword == 'cm':
            url = "http://%s.baoxian.in/test/index" % appname
        elif keyword == 'go':
            url = "http://go2.baoxian.com"
        elif keyword == 'carbiz':
            url = "http://%s.baoxian.in" % appname
        elif keyword == 'cx':
            url = "http://%s.baoxian.com" % appname
        elif keyword == 'rb':
            url = "http://%s.baoxian.in" % appname
        elif keyword == 'engine':
            url = "http://%s.baoxian.com" % appname
        elif appname == 'order':
            url = "http://go2.baoxian.com/order/00CF3730B98041A784C5B239DFD6A944/029000120000137701"
        elif appname == 'order2':
            url = "http://carbiz2.baoxian.in/order/7828F66CD6944AA591611951813313CD/0002020278140002956081"
        elif appname == 'order3':
            url = "http://carbiz3.baoxian.in/order/E35EEE3778944E8B8A683497F9AE1767/0002020333130000323331"
        elif appname == 'order4':
            url = "http://carbiz4.baoxian.in/order/722C3459FC154D8A8FF35DB76C6C84EE/0001029430140001674871"
        elif appname == 'order5':
            url = "http://carbiz5.baoxian.in/order/00CF3730B98041A784C5B239DFD6A944/029000120000137701"
        elif appname == 'order6':
            url = "http://carbiz6.baoxian.in/order/41508C1A6B0342C98529683E407471B7/020277120000004901"
        elif appname == 'dataTransform':
            url = "http://203.195.162.226:8080"
        elif appname == 'dataTransform2':
            url = "http://203.195.162.26:8081"
        elif appname == 'dataTransform3':
            url = "http://203.195.164.129:8081"
        elif appname == 'dataTransform4':
            url = "http://203.195.164.173:8080"
        elif appname == 'dataTransform5':
            url = "http://203.195.152.253:8080"
        elif appname == 'dataTransform6':
            url = "http://203.195.154.211:8080"
        #print url
        r = requests.get(url, allow_redirects = False)
        #return r.status_code
        if r.status_code == 200:
            return "Success"
        else:
            return "False"
