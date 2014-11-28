# coding: utf-8

import web
from models.models import getCityInfo
from models.models import getIDCInfo,getProjectInfo,getStatusInfo
#from config.setting import render_plain

def getIp():
	return web.ctx.env.get('REMOTE_ADDR')

#{'1': city,'2': city}
def cidToCity():
	all_city = getCityInfo()
	all_city_dict = {}
	for c in all_city:
		all_city_dict[c.cid] = c.city
	return all_city_dict

#{'1': idcname'}	
def iidToIDCName():
	all_idc = getIDCInfo()
	all_idc_dict = {}
	for i in all_idc:
		all_idc_dict[i.iid] = i.idcname
	return all_idc_dict

#{'1': project'}
def pidToProject():
	projects = getProjectInfo()
	projects_dict = {}
	for p in projects:
		projects_dict[p.pid] = p.project
	return projects_dict

def sidToStatus():
	status = getStatusInfo()
	status_dict = {}
	for s in status:
		status_dict[s.sid] = s.status
	return status_dict

def code(str):
	#return str.decode('utf-8').encode('gb2312')
	return str.decode('utf-8').encode('utf-8')

def code2(str):
	return str.decode('utf-8').encode('utf-8')

def logged():
	if web.ctx.session.logined != 0:
		return True
	else:
		return False

def checkIp(s):
    try:
        ip_add = s.split('.')
        if len(ip_add) != 4:
            return False
        else:
            for i in ip_add:
                if int(i) >= 255:
                    return False
                    break

        return True
    except:
        return  False

def isInt(s):
	try:
		a = int(s)
		return True
	except:
		return False

def checkPort(s):
	try:
		a = int(s)
		if a > 65535:
			return False
		return True	
	except:
		return False

def getCity(cid):
	city_dict = cidToCity()	
	if not city_dict.has_key(cid):
		return "Unknown"
	else:
		return city_dict[cid]

def getProject(pid):
	project_dict = pidToProject()	
	if not project_dict.has_key(pid):
		return "Unknown"
	else:
		return project_dict[pid]

def getIDC(iid):
	idc_dict = iidToIDCName()
	if not idc_dict.has_key(iid):
		return "Unknown"
	else:
		return idc_dict[iid]

def getStatus(sid):
	status_dict = sidToStatus()
	if not status_dict.has_key(sid):
		return "Unknown"
	else:
		return status_dict[sid]

def return500():
	#return web.notfound(render_plain.page500())
	raise web.seeother('/500')
	
def return404():
	#return web.notfound(render_plain.page404())
	raise web.seeother('/404')

def DownLoad(file):
	BUF_SIZE = 262144
	f = None		
	try:
		f = open('download/'+file,'rb')
		web.header('Content-Type','application/octet-stream')
		web.header('Content-disposition', 'attachment; filename=%s' % file)
		while True:
			c = f.read(BUF_SIZE)
			if c:
				yield c
			else:
				break
	except Exception, e:
		print e
		yield 'Error'
	finally:
		if f:
			f.close()
