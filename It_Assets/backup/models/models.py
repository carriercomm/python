# coding: utf-8
# Author Steven
import web
from config.setting import db

def insert_user(privilege,username,password,createtime,lastlogin,loginip,phone,email,other):
	db.insert('users',privilege=privilege,username=username,password=password,createtime=createtime,lastlogin=lastlogin,loginip=loginip,phone=phone,email=email,other=other)

def getUserInfo(username):
	try:
		#results = db.select('users', where="username=$username")
		results = db.query("SELECT * FROM `users` WHERE username='%s'" % (username))
		return results[0]
	except IndexError:
		return 0

def getUserInfoByUID(uid):
	try:
		results = db.query("SELECT * FROM `users` WHERE uid=%s" % (uid))
		return results[0]
	except IndexError:
		return 0

def updateUserLogin(uid, lastlogin, loginip):
	db.query("UPDATE `users` SET `lastlogin` = '%s', `loginip` = '%s' WHERE `uid` = %s;" %  (lastlogin, loginip, uid))

def UpdateUserInfo(user,phone,email,other):
	return db.update("users", where='username=$user', vars={'user':user}, phone=phone, email=email, other=other)

def UpdateUserPrivilege(user,privilege):
	return db.update("users", where='username=$user', vars={'user':user}, privilege=privilege)

def delUserByUID(uid):
	return db.delete("users", where='uid=$uid', vars={'uid': uid})

def ChangeUserPWD(user,pwd):
	db.query("UPDATE `users` SET `password` = '%s' WHERE `username` = '%s'" %  (pwd,user))

def hasUser(username):
	try:
		results = db.query("SELECT uid FROM `users` WHERE username='%s'" % (username))
		#return results[0]
		if results:
			return 1
	except IndexError:
		return 0

def insert_city(city, other):
	result = db.query("SELECT cid FROM `city` WHERE city='%s'" % (city))	
	if result:
		return False
	else:
		db.insert('city', city=city, other=other)
		return True

def insert_idc(idcname,city, contact,hztime, other):
	result = db.query("SELECT iid FROM `idc` WHERE idcname='%s'" % (idcname))
	if result:
		return False
	else:
		db.insert('idc', idcname=idcname, city=city, contact=contact,hztime=hztime, other=other)
		return True

def insert_project(project, other):
	result = db.query("SELECT pid FROM `project` WHERE project='%s'" % (project))
	if result:
		return False
	else:	
		db.insert('project', project=project, other=other)
		return True

def insert_host(hostname,city,project,idc,port,addr1_ip,addr1_netmask,addr1_gateway,addr1_line,addr2_ip,addr2_netmask,addr2_gateway,addr2_line,addr3_ip,addr3_netmask,addr3_gateway,addr3_line,memory,cpu,disk,buytime,servicetime,hardwareinfo,bandwidth,uses,status,company,os,other,jointime,modifytime,modifyman):

	# Check the ip address exists?
	if addr1_ip != '':
		result = db.query("SELECT hid FROM `hosts` WHERE addr1_ip='%s' OR addr2_ip='%s' OR addr3_ip='%s'" % (addr1_ip, addr1_ip, addr1_ip))
		if result:
			return False
	if addr2_ip != '':
		result = db.query("SELECT hid FROM `hosts` WHERE addr1_ip='%s' OR addr2_ip='%s' OR addr3_ip='%s'" % (addr2_ip, addr2_ip, addr2_ip))
		if result:
			return False
	if addr3_ip != '':
		result = db.query("SELECT hid FROM `hosts` WHERE addr1_ip='%s' OR addr2_ip='%s' OR addr3_ip='%s'" % (addr3_ip, addr3_ip, addr3_ip))
		if result:
			return False

	# If not enter the ip address, also saved to database.
	db.insert('hosts',hostname=hostname,city=city,project=project,idc=idc,port=port,addr1_ip=addr1_ip,addr1_netmask=addr1_netmask,addr1_gateway=addr1_gateway,addr1_line=addr1_line,addr2_ip=addr2_ip,addr2_netmask=addr2_netmask,addr2_gateway=addr2_gateway,addr2_line=addr2_line,addr3_ip=addr3_ip,addr3_netmask=addr3_netmask,addr3_gateway=addr3_gateway,addr3_line=addr3_line,memory=memory,cpu=cpu,disk=disk,buytime=buytime,servicetime=servicetime,hardwareinfo=hardwareinfo,bandwidth=bandwidth,uses=uses,status=status,company=company,os=os,other=other,jointime=jointime,modifytime=modifytime,modifyman=modifyman)
	return True

def getCidByHid(hid):
	result = db.query("select city from hosts,idc where hosts.idc = idc.iid and hid=%s" % hid)
	return result

def getProjectInfo():
	return db.query("SELECT * FROM `project`")

def getCityInfo():
	return db.query("SELECT * FROM `city`")
	
def getIDCInfo():
	return db.query("SELECT * FROM `idc`")

def getStatusInfo():
	return db.query("SELECT * FROM `status`")

def getOneIDC(iid):
	return db.query("SELECT * FROM `idc` WHERE iid='%s'" % (iid))

def getOneProject(pid):
	result = db.query("SELECT * FROM `project` WHERE pid='%s'" % (pid))
	return result[0]

def getAllHosts():
	return db.query("SELECT * FROM `hosts` ORDER BY project")
	
def getOneHost(hid):
	return db.query("SELECT * FROM `hosts` WHERE hid='%s'" % (hid))

def getOneCity(cid):
	return db.query("SELECT * FROM `city` WHERE cid='%s'" % (cid))

def delHost(hid):
	return db.query("DELETE FROM `hosts` WHERE hid='%s'" % (hid))

def modifyHost(hid,hostname,city,project,idc,port,addr1_ip,addr1_netmask,addr1_gateway,addr1_line,addr2_ip,addr2_netmask,addr2_gateway,addr2_line,addr3_ip,addr3_netmask,addr3_gateway,addr3_line,memory,cpu,disk,buytime,servicetime,hardwareinfo,bandwidth,uses,status,company,os,other,modifytime,modifyman):
	result = db.query("SELECT hid FROM hosts WHERE hostname = '%s' AND hid != '%s'" % (hostname, hid))
	if result:
		return False
	else:
		db.update("hosts", where='hid=$hid', vars={'hid':hid}, hostname=hostname,city=city,project=project,idc=idc,port=port,addr1_ip=addr1_ip,addr1_netmask=addr1_netmask,addr1_gateway=addr1_gateway,addr1_line=addr1_line,addr2_ip=addr2_ip,addr2_netmask=addr2_netmask,addr2_gateway=addr2_gateway,addr2_line=addr2_line,addr3_ip=addr3_ip,addr3_netmask=addr3_netmask,addr3_gateway=addr3_gateway,addr3_line=addr3_line,memory=memory,cpu=cpu,disk=disk,buytime=buytime,servicetime=servicetime,hardwareinfo=hardwareinfo,bandwidth=bandwidth,uses=uses,status=status,company=company,os=os,other=other,modifytime=modifytime,modifyman=modifyman)
		return True

def allHosts():
	all = db.query("SELECT count(*) as count FROM `hosts`")	
	return all[0].count

def getPage(offset, pagesize):
	result = db.query("SELECT * FROM `hosts` order by hid desc limit %s,%s" % (offset,pagesize))
	return result

def getPageByLastModify(offset, pagesize):
	result = db.query("SELECT * FROM `hosts` order by modifytime desc limit %s,%s" % (offset,pagesize))
	return result

def getHostCountByCity(cid):
	result = db.query("SELECT count(*) as count FROM `hosts` WHERE city = %s" % (cid))
	#result = db.query("select count(hid) as count from hosts,idc where hosts.idc = idc.iid and city = %s" % cid)
	return result[0].count
	
def getIDCCountByCity(cid):
	all = db.query("SELECT count(iid) as count FROM `idc` WHERE city = '%s'" % (cid))
	return all[0].count

def getHostCountByIDC(iid):
	all = db.query("SELECT count(hid) as count FROM `hosts` WHERE idc = '%s'" % (iid))
	return all[0].count

def getHostCountByProject(pid):
	all = db.query("SELECT count(hid) as count FROM `hosts` WHERE project = '%s'" % (pid))
	return all[0].count

def getIDCCountByProject(pid):
	all = db.query("SELECT count(distinct idc) as count FROM `hosts` WHERE project='%s'" % (pid))	
	return all[0].count

def modifyCity(cid, city, other):
	result = db.query("SELECT cid FROM city WHERE city = '%s' AND cid != '%s'" % (city, cid))
	if result:
		return False	
	else:
		db.update("city", where='cid=$cid', vars={'cid': cid}, city=city, other=other)
		return True

def delIDC(iid):
	return db.delete("idc", where='iid=$iid', vars={'iid': iid})

def delCity(cid):
	return db.delete("city", where='cid=$cid', vars={'cid': cid})

def delProject(pid):
	return db.delete("project", where='pid=$pid', vars={'pid': pid})

def modifyIDC(iid,idcname,city,contact,hztime,other):
	result = db.query("SELECT iid FROM idc WHERE idcname = '%s' AND iid != '%s'" % (idcname, iid))
	if result:
		return False
	else:
		db.update("idc", where='iid=$iid', vars={'iid': iid}, idcname=idcname, city=city, contact=contact, hztime=hztime,other=other)
		return True
	
def modifyProject(pid,project,other):
	result = db.query("SELECT pid FROM project WHERE project = '%s' AND pid != '%s'" % (project,pid))
	if result:
		return False
	else:
		db.update("project", where='pid=$pid', vars={'pid': pid}, project=project ,other=other)
		return True

def getHostByCity(cid):
	return db.query("SELECT *  FROM `hosts` WHERE city = '%s'" % (cid))
	
def getPageByCity(cid,offset, pagesize):
	result = db.query("SELECT * FROM `hosts` WHERE city = %s order by hid desc limit %s,%s" % (cid,offset,pagesize))
	#result = db.query("select *  from hosts,idc where hosts.idc = idc.iid and  city=%s order by hid desc limit %s,%s" % (cid,offset,pagesize))
	return result

def getPageByIDC(iid,offset, pagesize):
	result = db.query("SELECT * FROM `hosts` WHERE idc = %s order by hid desc limit %s,%s" % (iid,offset,pagesize))
	return result

def getPageByProject(pid,offset, pagesize):
	result = db.query("SELECT * FROM `hosts` WHERE project = %s order by hid desc limit %s,%s" % (pid,offset,pagesize))
	return result

def getIDCInfoByProject(pid):
	result = db.query("SELECT DISTINCT idc FROM `hosts` WHERE project = '%s'" % (pid))
	return result

def getHostCountByPidAndIid(pid,iid):
	result = db.query("SELECT count(hid) as count FROM `hosts` WHERE project = '%s' AND idc = '%s'" % (pid, iid))
	return result[0].count

def getPageByPidAndIid(pid,iid,offset,pagesize):
	result = db.query("SELECT * FROM `hosts` WHERE project = '%s' AND idc = '%s' order by hid desc limit %s,%s" % (pid,iid,offset,pagesize))
	return result

def getIDCInfoByCity(cid):
	result = db.query("SELECT * FROM `idc` WHERE city = '%s'" % (cid))
	return result

def getHostCountByCidAndIid(cid,iid):
	result = db.query("SELECT count(hid) as count FROM `hosts` WHERE city = '%s' AND idc = '%s'" % (cid, iid))
	#result = db.query("select count(hid) as count from hosts,idc where hosts.idc = idc.iid and idc=%s and city=%s" % (iid, cid))
	return result[0].count

def getHostCountBySearch(field,keyword):
	result = db.query("SELECT count(hid) as count FROM `hosts` WHERE "+ field +" LIKE '%"+ keyword +"%'")
	return result[0].count

def getHostCountBySearchIp(ip):
	result = db.query("SELECT COUNT(hid) as count FROM `hosts` WHERE addr1_ip LIKE '%"+ip+"%' OR addr2_ip LIKE '%"+ip+"%' OR addr3_ip LIKE '%"+ip+"%'")
	return result[0].count

def getPageBySearch(field,keyword,offset,pagesize):
	result = db.query("SELECT * FROM `hosts` WHERE "+ field +" LIKE '%"+ keyword +"%' limit "+offset+","+pagesize+"")
	return result

def getPageBySearchIp(ip,offset,pagesize):
	result = db.query("SELECT * FROM `hosts` WHERE addr1_ip LIKE '%"+ip+"%' OR addr2_ip LIKE '%"+ip+"%' OR addr3_ip LIKE '%"+ip+"%' limit "+offset+","+pagesize+"")
	return result

def getUserList():
	return db.select('users', order="lastlogin DESC")

def getConfig():
	query = db.select('config')
	return query[0]

def updateConfig(name,page):
	return db.query("UPDATE config SET name='%s',page='%s' LIMIT 1;" % (name, page))

def getSysOverView():
	result = db.query("SELECT COUNT(hid) AS host,COUNT(distinct city) AS city,COUNT(distinct idc) AS idc,COUNT(distinct project) AS project FROM hosts")
	return result[0]

def getStatusOverView():
	result = db.query("select distinct hosts.status as sid,status.status,count(hosts.status) as total from hosts,status where hosts.status = status.sid group by hosts.status")
	return result

def getHistory():
	result = db.query("SELECT * FROM history ORDER BY deltime desc")
	return result

def restoreHistory(hid):
	content = db.query("SELECT content FROM history WHERE hid = %s" % hid)
	try:
		sql = content[0]['content']
		result = db.query("%s" % sql)
	except:
		return False

	if result:
		return True
	else:
		return False

def addHistory(content,description,delman,deltime):
	db.insert('history',content=content,description=description,delman=delman,deltime=deltime)

def delOneHistory(hid):
	return db.delete("history", where='hid=$hid', vars={'hid': hid})
