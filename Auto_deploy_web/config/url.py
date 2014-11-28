#!/bin/env python
# coding: utf-8

import web,os

pre_fix = 'controllers.'

urls = (
    '/',                    pre_fix + 'todo.Login',
    '/logout',              pre_fix + 'todo.Logout',
    '/main',                pre_fix + 'todo.Main',
    '/app',                 pre_fix + 'todo.App',
    '/userlist',            pre_fix + 'todo.UserList',
    '/register',            pre_fix + 'todo.Register',
    '/muser',               pre_fix + 'todo.ModifyUserInfo',
    '/sysinfo',             pre_fix + 'todo.SysInfo',

)


