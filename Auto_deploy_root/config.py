# -*- coding:utf8 -*-
import os
from tornado import template

#指定配置文件及软件的目录
template_path=os.path.join(os.path.dirname(__file__), "configuredir/")
softs_path = os.path.join(os.path.dirname(__file__), "softdir/")
rollback_dir = os.path.join(os.path.dirname(__file__), "rollbackdir/")
deploy_dir = os.path.join(os.path.dirname(__file__), "deploydir/")

rsync_server = "10.143.76.210"
#rsync_server = "121.14.57.241"
port = 22

values_dict = {
"engine_ip":"",}

app_dict = {
"cipm":{"ip":"10.143.78.178","dir":"/data/www/","type":"resin"},
"cipm2":{"ip":"10.232.27.100","dir":"/data/www/","type":"resin"},
"cipm3":{"ip":"10.143.76.90","dir":"/data/www/","type":"resin"},
"cipm4":{"ip":"10.143.66.193","dir":"/data/www/","type":"resin"},
"cipm5":{"ip":"10.143.74.116","dir":"/data/www/","type":"resin"},
"cipm6":{"ip":"10.143.106.130","dir":"/data/www/","type":"resin"},
"cx":{"ip":"10.143.80.190","dir":"/data/www/","type":"resin"},
"cx2":{"ip":"10.143.72.81","dir":"/data/www/","type":"resin"},
"cx3":{"ip":"10.143.96.41","dir":"/data/www/","type":"resin"},
"cx4":{"ip":"10.143.96.40","dir":"/data/www/","type":"resin"},
"cx5":{"ip":"10.143.72.63","dir":"/data/www/","type":"resin"},
"cx6":{"ip":"10.143.80.141","dir":"/data/www/","type":"resin"},
"cm":{"ip":"10.143.84.184","dir":"/data/www/","type":"resin"},
"cm2":{"ip":"10.143.78.189","dir":"/data/www/","type":"resin"},
"cm3":{"ip":"10.143.86.113","dir":"/data/www/","type":"resin"},
"cm4":{"ip":"10.143.68.237","dir":"/data/www/","type":"resin"},
"cm5":{"ip":"10.221.38.220","dir":"/data/www/","type":"resin"},
"cm6":{"ip":"10.143.94.42","dir":"/data/www/","type":"resin"},
"go2":{"ip":"10.143.72.245","dir":"/data/www/","type":"resin"},
"carbiz2":{"ip":"10.143.72.247","dir":"/data/www/","type":"resin"},
"carbiz3":{"ip":"10.143.86.109","dir":"/data/www/","type":"resin"},
"carbiz4":{"ip":"10.143.88.47","dir":"/data/www/","type":"resin"},
"carbiz5":{"ip":"10.221.38.8","dir":"/data/www/","type":"resin"},
"carbiz6":{"ip":"10.143.96.29","dir":"/data/www/","type":"resin"},
"rb":{"ip":"10.143.74.202","dir":"/data/www/","type":"resin"},
"rb2":{"ip":"10.143.78.190","dir":"/data/www/","type":"resin"},
"rb3":{"ip":"10.143.84.192","dir":"/data/www/","type":"resin"},
"rb4":{"ip":"10.143.84.195","dir":"/data/www/","type":"resin"},
"rb5":{"ip":"10.221.39.85","dir":"/data/www/","type":"resin"},
"rb6":{"ip":"10.143.94.41","dir":"/data/www/","type":"resin"},
"engine":{"ip":"10.143.78.177","dir":"/data/www/","type":"resin"},
"engine2":{"ip":"10.232.63.99","dir":"/data/www/","type":"resin"},
"engine3":{"ip":"10.143.96.42","dir":"/data/www/","type":"resin"},
"engine4":{"ip":"10.143.94.48","dir":"/data/www/","type":"resin"},
"engine5":{"ip":"10.143.78.77","dir":"/data/www/","type":"resin"},
"engine6":{"ip":"10.143.72.210","dir":"/data/www/","type":"resin"},
"dataTransform":{"ip":"10.143.78.185","dir":"/data/www/","type":"resin"},
"dataTransform2":{"ip":"10.143.72.246","dir":"/data/www/","type":"resin"},
"dataTransform3":{"ip":"10.143.84.60","dir":"/data/www/","type":"resin"},
"dataTransform4":{"ip":"10.143.86.110","dir":"/data/www/","type":"resin"},
"dataTransform5":{"ip":"10.232.66.79","dir":"/data/www/","type":"resin"},
"dataTransform6":{"ip":"10.143.90.252","dir":"/data/www/","type":"resin"},
"order":{"ip":"10.143.82.193","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"order2":{"ip":"10.143.68.239","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"order3":{"ip":"10.143.84.193","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"order4":{"ip":"10.143.78.193","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"order5":{"ip":"10.221.39.118","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"order6":{"ip":"10.221.39.153","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"radar":{"ip":"10.143.86.231","dir":"/data/www/apps/","type":"app","start":"sh /data/www/apps/radar/bin/boxrun srvbox-radar","stop":"/etc/init.d/radarstop"},
"radar2":{"ip":"10.143.73.16","dir":"/data/www/apps/","type":"app","start":"sh /data/www/apps/radar/bin/boxrun srvbox-radar","stop":"/etc/init.d/radarstop"},
"radar3":{"ip":"10.143.73.14","dir":"/data/www/apps/","type":"app","start":"sh /data/www/apps/radar/bin/boxrun srvbox-radar","stop":"/etc/init.d/radarstop"},
"radar4":{"ip":"10.207.163.109","dir":"/data/www/apps/","type":"app","start":"sh /data/www/apps/radar/bin/boxrun srvbox-radar","stop":"/etc/init.d/radarstop"},
"radar5":{"ip":"10.232.64.73","dir":"/data/www/apps/","type":"app","start":"sh /data/www/apps/radar/bin/boxrun srvbox-radar","stop":"/etc/init.d/radarstop"},
"radar6":{"ip":"10.232.65.25","dir":"/data/www/apps/","type":"app","start":"sh /data/www/apps/radar/bin/boxrun srvbox-radar","stop":"/etc/init.d/radarstop"},
"renewal":{"ip":"10.143.78.188","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"renewal2":{"ip":"10.143.72.248","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"renewal3":{"ip":"10.143.86.108","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"renewal4":{"ip":"10.143.74.206","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"renewal5":{"ip":"10.221.38.219","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"renewal6":{"ip":"10.143.94.40","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"task-dispatcher":{"ip":"10.143.76.216","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/dispatcher","stop":"stop"},
"task-dispatcher2":{"ip":"10.143.84.185","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/dispatcher","stop":"stop"},
"task-dispatcher3":{"ip":"10.143.84.189","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/dispatcher","stop":"stop"},
"task-dispatcher4":{"ip":"10.143.88.46","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/dispatcher","stop":"stop"},
"task-dispatcher5":{"ip":"10.143.94.38","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/dispatcher","stop":"stop"},
"task-dispatcher6":{"ip":"10.143.94.43","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/dispatcher","stop":"stop"}
           }
