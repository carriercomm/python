# -*- coding=utf-8 -*-

from fabric.api import *
from fabric.contrib.project import rsync_project

env.roledefs = {
    'liantong':[ #电信机房
        'xxx@w01v.add.xxx.com',
        'xxx@w02v.add.xxx.com',
    ],
    'dianxin':[ #联通机房
        'xxx@w01v.add.xxx.com',
        'xxx@w02v.add.xxx.com',
    ],
}

@roles('liantong', 'dianxin') #这么写装饰器是表示电信，联通都要执行这个函数
def check():
    run('ps aux | grep uwsgi | grep -v grep')
    run('ls -l /home/system/service/')

def initFiles(): 
    execute(liantong_conf) #执行 liantong_conf()
    execute(dianxin_conf)  #执行 dianxin_conf()

@roles('dianxin') 	#电信
def dianxin_conf():
    initFiles1()
    sudo("cd /home/system/service && mv settings_online_dianxin.py settings.py")
    initFiles2()

@roles('liantong') 	#联通
def liantong_conf():
    initFiles1()
    sudo("cd /home/system/service && mv settings_online_liantong.py settings.py")
    initFiles2()

@roles('liantong', 'dianxin')
def initFiles1():
    sudo("chmod 777 /home/system/service")
    sudo("chmod 777 /home/system/service/orm")
    sudo("chown -R auxten:auxten /home/system/service")

    rsync_project( # 调用rsync
        remote_dir='/home/system/service/',
        local_dir='/Users/auxten/Codes/Web/flow-web/*',
        exclude=['python2.7','*.pyc','*.log','.svn','.idea','logs','*pull.sh','*push.sh','settings.py']
    )

@roles('liantong', 'dianxin')
def initFiles2():
    sudo("chown -R apache:apache /home/system/service")

@roles('liantong', 'dianxin')
def restart():
    sudo("sh /home/system/service/run.sh")
    run('ps aux | grep uwsgi | grep -v grep')

@roles('liantong', 'dianxin')
def checkLog():
    sudo('tail -50 /home/system/service/uwsgi.log')

#上线就只需执行
#fab -f webDeploy.py initFiles restart #即可，登陆密码和sudo密码都只会问一遍
