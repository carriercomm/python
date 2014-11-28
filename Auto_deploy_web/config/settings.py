#!/bin/env python
# coding: utf-8
import web
import os
from url import urls

# Define database connection
db = web.database(dbn='mysql', db='yunwei', user='yunwei', pw='yunwei',unix_socket="/tmp/mysql.sock")

render = web.template.render('templates/', cache=False)

web.config.debug = True

config = web.storage(
    email='qichangxing@gmail.com',
    site_name = '任务跟踪',
    site_desc = '',
    static = '/static',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render


# Loading system config
app = web.application(urls, globals())

# Define sessions
curdir = os.path.dirname(__file__)

if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir, 'sessions')), initializer={'logined': 0, 'uid': 0, 'username': '', 'privilege': 0})
	web.config._session = session
else:
	session = web.config._session

def session_hook():
	web.ctx.session = session

app.add_processor(web.loadhook(session_hook))