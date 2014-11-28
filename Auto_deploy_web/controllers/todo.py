#!/bin/env python
# coding: utf-8
import subprocess
import web, sys, time, hashlib, os, xlwt
from  models import models
import base
from config import settings
from  models import models
#from datetime import datetime

render = settings.render
#db = settings.db
#tb = 'todo'



class Login:

    def GET(self):
        #todos = db.select(tb, order='finished asc, id asc')
        #return render.index()
        #print web.ctx.session.logined
        #print base.logged()
        if base.logged():
            raise web.seeother('/main')
        else:
            return render.login()
    def POST(self):
        username = web.input().username
        password = web.input().password
        hash_password = hashlib.new('md5', password+'Steven').hexdigest()
        user_info = models.getUserInfo(username)

        if user_info:
            if user_info['password'] != hash_password:
                return base.code("<script language='javascript'>alert('密码错误');window.history.back(-1);</script>")
            else:
                # Create session
                web.ctx.session.logined = 1
                web.ctx.session.uid = user_info['uid']
                web.ctx.session.username = user_info['username']
                web.ctx.session.privilege = user_info['privilege']

                # Update user info
                clientip = base.getIp()
                models.updateUserLogin(web.ctx.session.uid, int(time.time()), clientip)
                raise web.seeother('/main')

class Logout:
    def GET(self):
        web.ctx.session.kill()
        raise web.seeother('/')

class UserList:
    def GET(self):
        if not base.logged():
            raise web.seeother('/')
        user_list = models.getUserList()
        #username,privi,phone,email,logintime,loginip
        user_info_list = []
        for u in user_list:
            if u['lastlogin'] != '':
                ltime = time.localtime(int(u['lastlogin']))
                lastlogin = time.strftime("%Y-%m-%d %H:%M:%S",ltime)
            else:
                lastlogin = ''
            u['lastlogin'] = lastlogin
            user_info_list.append(u)
        #print web.ctx.session.privilege
        if web.ctx.session.privilege == 2:
            return  render.user_list_admin(user_info_list)
        else:
            return  render.user_list(user_info_list)

class Main:

    def GET(self):
        #todos = db.select(tb, order='finished asc, id asc')
        #print web.ctx.session.username
        return render.index(web.ctx.session.username)
        #return render.login()

class App:

    def GET(self):
        #todos = db.select(tb, order='finished asc, id asc')
        return render.app()

    def POST(self):
        #todos = db.select(tb, order='finished asc, id asc')
        n = web.input()
        #print n
        cmd = ''
        opt = n["operator"]
        del n["operator"]
        del n["'"]
        print n
        if n:
            for k in n.values():
                cmd =cmd+' '+k
            if opt == "deploy":
                print "%s %s '%s'" %("-d","--part",cmd)
                output = subprocess.check_output("cat /data/test.txt", shell=True)
            elif opt=="rollback":
                print "%s %s '%s'" %("-r","--part",cmd)
                output = subprocess.check_output("cat /etc/hosts", shell=True)
        else:
            print "请选择要发布的应用"
            output = "您没有选择任何应用，请在需要发布的应用前打勾！"

        data = output.split("\n")
        #print output, data

        return render.deploy_log(data)


class Register:
    def GET(self):
        if not base.logged():
            raise web.seeother('/')
        if web.ctx.session.privilege != 2:
            return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
        else:
            return render.register()

    def POST(self):
        # Privilege  0: reader 1: read and write 2: administrator
        privilege = int(web.input().privilege)
        username = web.input().username.strip()
        password = web.input().password
        password2 = web.input().password2
        phone = web.input().phone.strip()
        email = web.input().email.strip()
        other = web.input().other

        if username == '':
            return base.code("<script language='javascript'>alert('请输入用户名');window.history.back(-1);</script>")
        elif password == '':
            return base.code("<script language='javascript'>alert('请输入密码');window.history.back(-1);</script>")
        elif models.hasUser(username) == 1:
            return base.code("<script language='javascript'>alert('该用户已存在');window.history.back(-1);</script>")
        elif password != password2:
            #return base.code("密码不匹配，请重新输入!")
            return base.code("<script language='javascript'>alert('密码不匹配，请重新输入!');window.history.back(-1);</script>")
        elif web.ctx.session.privilege != 2:
            return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
        else:
            newpassword = hashlib.new('md5', password+'Steven').hexdigest()
            #insert_user(privilege,username,password,createtime,lastlogin,loginip,phone,email,other)
            models.insert_user(privilege,username,newpassword,int(time.time()),'','',phone,email,other)
            raise web.seeother('/userlist')

class ModifyUserInfo:
    def GET(self):
        if not base.logged():
            raise web.seeother('/')
        input = web.input()
        if input.action == "vu":
            user_info = models.getUserInfoByUID(input.uid)
            return render.view_user(user_info)
        elif input.action == "mu":
            if web.ctx.session.privilege == 2:
                user_info = models.getUserInfoByUID(input.uid)
                return render.modify_user_admin(user_info)
            else:
                user_info = models.getUserInfoByUID(web.ctx.session.uid)
                return render.modify_user(user_info)
        elif input.action == 'du':
            if web.ctx.session.privilege != 2:
                return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")
            models.delUserByUID(input.uid)
            raise web.seeother('/userlist')
        else:
            return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")


    def POST(self):
        input = web.input()
        # User is admin
        if web.ctx.session.privilege == 2:
            if input.password != '':
                if input.password2 != input.password:
                    return base.code("<script language='javascript'>alert('密码不匹配 !');window.history.back(-1);</script>")
                else:
                    new_pwd = hashlib.new('md5', input.password+'Steven').hexdigest()
                    models.ChangeUserPWD(input.username.strip(),new_pwd)
            models.UpdateUserInfo(input.username.strip(),input.phone.strip(),input.email.strip(),input.other)
            models.UpdateUserPrivilege(input.username.strip(),input.privilege)
            raise web.seeother('/userlist')

class SysInfo:
    def GET(self):
        if not base.logged():
            raise web.seeother('/')
        return  render.sysinfo()
