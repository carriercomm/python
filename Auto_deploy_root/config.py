# -*- coding:utf8 -*-
import os
from tornado import template

#指定配置文件及软件的目录
template_path=os.path.join(os.path.dirname(__file__), "configuredir/")
softs_path = os.path.join(os.path.dirname(__file__), "softdir/")
rollback_dir = os.path.join(os.path.dirname(__file__), "rollbackdir/")
deploy_dir = os.path.join(os.path.dirname(__file__), "deploydir/")

rsync_server = "10.232.62.100"
port = 22

values_dict = {
"engine_ip":"10.68.3.116","printer_ip":"10.68.3.99","order1_ip":"10.68.3.86","order3_ip":"10.68.3.52","cipm_ip":"10.68.3.24","database_ip":"10.68.3.228","codetable_ip":"10.68.3.59","tc_ip":"10.68.3.63","ice_ip":"10.68.3.43","ldap_ip":"10.68.3.67","renewal_ip":"10.68.3.70","renewal3_ip":"10.68.3.51","cx_ip":"10.68.3.54","coherence1_ip":"10.68.3.85","coherence2_ip":"10.68.3.74","coherence3_ip":"10.68.3.88","coherence4_ip":"10.68.3.51","go21_ip":"10.68.3.85","carbiz3_ip":"10.68.3.30","tc3_ip":"10.68.3.53","message_ip":"10.68.3.226","scheduler_ip":"10.68.3.40","cm_ip":"10.68.3.22","cm3_ip":"10.68.3.27","seq_ip":"10.68.3.61","message3_ip":"10.68.3.249","seq3_ip":"192.168.100.243","imadmin_ip":"10.68.3.241","print_ip":"10.68.3.99","print3_ip":"10.68.3.64","cdm_ip":"10.68.3.239","orderTrack_ip":"10.68.3.94",

"cm_url":"cm.52zzb.com","sso_url":"sso.52zzb.com","ccm_url":"ccm.b2b.52zzb.com","go2_url":"go2.52zzb.com","picture_url":"picture.52zzb.com","cx_url":"cx.52zzb.com","engine_url":"engine.52zzb.com","atm_url":"atm.52zzb.com","jira1_url":"task.52zzb.com","cipm_url":"cipm.52zzb.com","cm3_url":"cm3.52zzb.com","carbiz3_url":"carbiz3.52zzb.com","jira3_url":"task3.52zzb.com","zone_tj":"tj","zone_gd":"gd","ssogo_url":"ssogo.52zzb.com"}

app_dict = {
"cipm":{"ip":"10.232.96.83","dir":"/data/www/","type":"resin"},
"cm":{"ip":"10.68.3.22","dir":"/data/www/","type":"resin"},
"cm3":{"ip":"10.68.3.27","dir":"/data/www/","type":"resin"},
"cm4":{"ip":"10.232.96.91","dir":"/data/www/","type":"resin"},
"go2":{"ip":"10.68.3.85","dir":"/data/www/","type":"resin"},
"carbiz3":{"ip":"10.68.3.30","dir":"/data/www/","type":"resin"},
"carbiz4":{"ip":"10.232.58.110","dir":"/data/www/","type":"resin"},
"rb":{"ip":"10.68.3.90","dir":"/data/www/","type":"resin"},
"rb3":{"ip":"10.68.3.26","dir":"/data/www/","type":"resin"},
"cx":{"ip":"10.232.70.116","dir":"/data/www/","type":"resin"},
"engine":{"ip":"10.68.3.116","dir":"/data/www/","type":"resin"},
"order3":{"ip":"10.68.3.52","dir":"/data/www/apps/","type":"app","start":"/data/www/apps/order-service-server/order.sh start","stop":"/data/www/apps/order-service-server/order.sh stop"},
"order4":{"ip":"10.232.4.53","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/order start","stop":"/etc/init.d/order stop"},
"radar4":{"ip":"10.232.74.116","dir":"/data/www/apps/","type":"app","start":"/etc/init.d/radar start","stop":"/etc/init.d/radar stop"                    }
           }
