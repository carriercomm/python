# coding: utf-8
# Author Steven
import web
from url import session

# Define database connection
db = web.database(dbn='mysql', db='yunwei', user='yunwei', pw='yunwei',unix_socket="/tmp/mysql.sock")

# Loading config from database
result = db.select('config')
sysconf = result[0]
#sysconf = models.getConfig()

# Debug
web.config.debug = True

# Loading templates
render = web.template.render('templates', base='base')
render_plain = web.template.render('templates')
web.template.Template.globals['session'] = session
web.template.Template.globals['int'] = int
web.template.Template.globals['sysconf'] = sysconf

