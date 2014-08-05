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
"engine_ip":"","printer_ip":"","order1_ip":"192.168.100.242","order2_ip":"192.168.100.65","cipm_ip":"","database_ip":"192.168.100.228","codetable_ip":"192.168.100.11","tc_ip":"192.168.100.13","ice_ip":"192.168.100.11","ldap_ip":"192.168.100.240","renewal_ip":"121.14.57.227","renewal2_ip":"113.108.228.50","cx_ip":"","coherence1_ip":"192.168.100.235","coherence2_ip":"192.168.100.230","coherence3_ip":"192.168.100.49","coherence4_ip":"192.168.100.24","go21_ip":"","carbiz2_ip":"","tc2_ip":"192.168.100.14","message_ip":"","scheduler_ip":"","cm_ip":"","cm2_ip":"","seq_ip":"","message2_ip":"","seq2_ip":"","imadmin_ip":"","print_ip":"","print2_ip":"","cdm_ip":"","orderTrack_ip":"",

"cm_url":"cm.baoxian.in","sso_url":"","ccm_url":"","go2_url":"go2.baoxian.com","picture_url":"","cx_url":"","engine_url":"","atm_url":"atm.baoxian.in","jira1_url":"task.baoxian.in","cipm_url":"","cm2_url":"cm2.baoxian.in","carbiz2_url":"carbiz2.baoxian.in","jira2_url":"task2.baoxian.in","zone_tj":"","zone_gd":"","ssogo_url":"","imadmin_url":"im.baoxian.in"}

app_dict = {
"cipm":{"ip":"192.168.100.234","dir":"/data/www/","type":"resin"},
"cx":{"ip":"192.168.100.48","dir":"/data/www/","type":"resin"},
"cm":{"ip":"10.143.84.184","dir":"/data/www/","type":"resin"},
"cm2":{"ip":"192.168.100.23","dir":"/data/www/","type":"resin"},
"go2":{"ip":"192.168.100.227","dir":"/data/www/","type":"resin"},
"carbiz2":{"ip":"192.168.100.25","dir":"/data/www/","type":"resin"},
"rb":{"ip":"192.168.100.17","dir":"/data/www/","type":"resin"},
"rb2":{"ip":"192.168.100.55","dir":"/data/www/","type":"resin"},
"engine":{"ip":"10.68.3.116","dir":"/data/www/","type":"resin"},
"order":{"ip":"192.168.100.242","dir":"/data/www/apps/","type":"app","start":"/data/www/apps/order-service-server/order.sh start","stop":"/data/www/apps/order-service-server/order.sh stop"},
"order2":{"ip":"192.168.100.65","dir":"/data/www/apps/","type":"app","start":"/data/www/apps/order-service-server/order.sh start","stop":"/data/www/apps/order-service-server/order.sh stop"},
"radar":{"ip":"192.168.100.17","dir":"/data/www/apps/","type":"app","start":"/data/www/apps/radar/bin/boxrun srvbox-radar &","stop":"stop"},
"radar2":{"ip":"192.168.100.55","dir":"/data/www/apps/","type":"app","start":"/data/www/apps/radar/bin/boxrun srvbox-radar &","stop":"stop"},
"renewal":{"ip":"10.143.78.188","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"},
"renewal2":{"ip":"10.143.72.248","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/renewal start","stop":"/etc/init.d/renewal stop"}
           }
