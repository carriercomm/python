# coding: utf-8
# Author Steven
import web, sys, time, hashlib, os, xlwt
from  models import models
import base
from config.setting import render
from config.setting import render_plain
from config.setting import sysconf

class Main:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		else:
			# Paging
			sysconf = models.getConfig()
			pagesize = sysconf['page']  # page_per_rows
			hostcount = models.allHosts()  # host_count
			para = web.input(page=None,action=None)	
			pages = int(hostcount / pagesize)	# page_count

			if (hostcount % pagesize):
				pages += 1				#page_count

			if para.page:
				if not para.page.isdigit():
					return base.code("<script language='javascript'>alert('参数错误');window.history.back(-1);</script>")
				page = int(para.page)
			else:
				page = 1

			offset = pagesize * (page - 1)  # offset
			
			if para.action:
				pagerows = models.getPageByLastModify(offset, pagesize)
			else:
				pagerows = models.getPage(offset, pagesize)

			newhosts=[]
			for h in pagerows:
				h['project'] = base.getProject(h['project'])
				h['city'] = base.getCity(h['city'])
				h['idc'] = base.getIDC(h['idc'])
				h['status'] = base.getStatus(h['status'])
				newhosts.append(h)

			#page Nav
			if hostcount <= pagesize:
				page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
			elif page == 1:
				page_nav = u"<a href='/main?page=%d'>下一页</a> | <a href='/main?page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (page+1,pages,page,pages,hostcount)
			elif page == pages:
				page_nav = u"<a href='/main?page=%d'>上一页</a> | <a href='/main?page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (page-1, page, pages,hostcount)
			else:
				page_nav = u"<a href='/main?page=%d'>下一页</a> | <a href='/main?page=%d'>上一页</a> | <a href='/main?page=1'>首页</a> | <a href='/main?page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (page+1,page-1,pages,page,pages,hostcount)
				
			if web.ctx.session.privilege == 0:
				return render.main(newhosts,pages,page,page_nav)
			else:
				return render.main_admin(newhosts,pages,page,page_nav)

class Login:
	def GET(self):
		if base.logged():
			raise web.seeother('/main')
		else:
			return render_plain.login()

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
		else:
			return base.code("<script language='javascript'>alert('用户不存在');window.history.back(-1);</script>")

class Logout:
	def GET(self):
		web.ctx.session.kill()
		raise web.seeother('/')

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
			return base.code("密码不匹配，请重新输入!")
		elif web.ctx.session.privilege != 2:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
		else:	
			newpassword = hashlib.new('md5', password+'Steven').hexdigest()

			#insert_user(privilege,username,password,createtime,lastlogin,loginip,phone,email,other):
			models.insert_user(privilege,username,newpassword,int(time.time()),'','',phone,email,other)
			raise web.seeother('/userlist')
			
class AddCity:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		if web.ctx.session.privilege == 0:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
		else:
			return render.add_city()
	
	def POST(self):
		city = web.input().city.strip()
		other = web.input().other

		if city == '':
			return base.code("<script language='javascript'>alert('请输入城市名称!');window.history.back(-1);</script>")

		result = models.insert_city(city, other)
		if result:
			raise web.seeother('/citylist')
		else:
			return base.code("<script language='javascript'>alert('该城市已存在!');window.history.back(-1);</script>")
		
class AddIDC:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		city = models.getCityInfo()

		if web.ctx.session.privilege == 0:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
		else:
			return render.add_idc(city)
	
	def POST(self):
		#idcname, city, contact, hztime, other =  web.input().idcname, web.input().contact, web.input().other
		datas = web.input()
	
		if datas.idcname == '':
			return base.code("<script language='javascript'>alert('请输入IDC名称!');window.history.back(-1);</script>")
			
		# Save to database
		result = models.insert_idc(datas.idcname.strip(), datas.city, datas.contact.strip(), datas.hztime, datas.other)
		if result:
			raise web.seeother('/idclist')
		else:
			return base.code("<script language='javascript'>alert('该IDC已存在!');window.history.back(-1);</script>")
	
class AddProject:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		
		if web.ctx.session.privilege == 0:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
		else:
			return render.add_project()

	def POST(self):
		project, other = web.input().project.strip(), web.input().other
		if project == '':
			return base.code("<script language='javascript'>alert('请输入项目名称!');window.history.back(-1);</script>")
		result = models.insert_project(project, other)
		if result:
			raise web.seeother('/projectlist')
		else:
			return base.code("<script language='javascript'>alert('该项目已存在!');window.history.back(-1);</script>")
		
class AddHost:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		city = models.getCityInfo()
		project = models.getProjectInfo()
		idc = models.getIDCInfo()
		status = models.getStatusInfo()
		
		if web.ctx.session.privilege == 0:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问!');window.history.back(-1);</script>")
		else:
			return render.add_host(city,project, idc, status)

	def POST(self):
		hostname = web.input().hostname.strip()
		city = web.input().city
		project = web.input().project
		idc = web.input().idc
		port = web.input().port.strip()
		addr1_ip = web.input().addr1_ip.strip()
		addr1_netmask = web.input().addr1_netmask.strip()
		addr1_gateway = web.input().addr1_gateway.strip()
		addr1_line = web.input().addr1_line.strip()
		addr2_ip = web.input().addr2_ip.strip()
		addr2_netmask = web.input().addr2_netmask.strip()
		addr2_gateway = web.input().addr2_gateway.strip()
		addr2_line = web.input().addr2_line.strip()
		addr3_ip = web.input().addr3_ip.strip()
		addr3_netmask = web.input().addr3_netmask.strip()
		addr3_gateway = web.input().addr3_gateway.strip()
		addr3_line = web.input().addr3_line.strip()

		memory = web.input().memory.strip()
		cpu = web.input().cpu.strip()
		disk = web.input().disk.strip()
		buytime = web.input().buytime
		servicetime = web.input().servicetime
		hardwareinfo = web.input().hardwareinfo
		bandwidth = web.input().bandwidth.strip()
		uses = web.input().uses.strip()
		status = web.input().status
		company = web.input().company.strip()
		os = web.input().os.strip()
		other = web.input().other

		# Input check
		if hostname == '':
			return base.code("<script language='javascript'>alert('主机标识必须输入 !');window.history.back(-1);</script>")
		if port != '':	
			if not base.checkPort(port):
				return base.code("<script language='javascript'>alert('端口不合法，请检查 !');window.history.back(-1);</script>")
	
		for ip in addr1_ip,addr1_gateway,addr2_ip,addr2_gateway,addr3_ip,addr3_gateway:
			if ip != '':
				if not base.checkIp(ip):
					return base.code("<script language='javascript'>alert('IP地址不合法，请检查 !');window.history.back(-1);</script>")
		for i in cpu,memory,disk:
			if i != '':
				if not base.isInt(i):
					return base.code("<script language='javascript'>alert('CPU/MEMORY/DISK不合法，请检查 !');window.history.back(-1);</script>")

		# Save host to db
		result = models.insert_host(hostname,city,project,idc,port,addr1_ip,addr1_netmask,addr1_gateway,addr1_line,addr2_ip,addr2_netmask,addr2_gateway,addr2_line,addr3_ip,addr3_netmask,addr3_gateway,addr3_gateway,memory,cpu,disk,buytime,servicetime,hardwareinfo,bandwidth,uses,status,company,os,other,int(time.time()),'',web.ctx.session.username)
		if result:
			raise web.seeother('/main')
		else:
			return base.code("<script language='javascript'>alert('IP已存在，请检查 !');window.history.back(-1);</script>")
		
class ModifyHosts:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		if not web.input():
			raise web.seeother('/main')

		action = web.input().action
		hid = web.input().hid
		if not hid.isdigit():
			return base.code("<script language='javascript'>alert('参数错误');window.history.back(-1);</script>")

		host = models.getOneHost(hid)
		if action == 'mh':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")
			city = models.getCityInfo()
			project = models.getProjectInfo()
			idc = models.getIDCInfo()
			status = models.getStatusInfo()
			return render.modify_host(city,project,idc,status,host[0])
		elif action == 'vh':
			city = models.getCityInfo()
			project = models.getProjectInfo()
			idc = models.getIDCInfo()
			status = models.getStatusInfo()
			host_list = list(host)
			t = host_list[0]['modifytime']
			ltime = time.localtime(int(t))
			modifytime = time.strftime("%Y-%m-%d %H:%M:%S",ltime)
			host_list[0]['modifytime'] = modifytime
			
			return render.view_host(city,project,idc,status,host_list[0])
		elif action == 'dh':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")
			
			# Save to history
			h = models.getOneHost(hid)[0]
			content = "INSERT INTO hosts VALUES (%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (h['hid'],h['hostname'],h['city'],h['project'],h['idc'],h['port'],h['addr1_ip'],h['addr1_netmask'],h['addr1_gateway'],h['addr1_line'],h['addr2_ip'],h['addr2_netmask'],h['addr2_gateway'],h['addr2_line'],h['addr3_ip'],h['addr3_netmask'],h['addr3_gateway'],h['addr3_gateway'],h['memory'],h['cpu'],h['disk'],h['buytime'],h['servicetime'],h['hardwareinfo'],h['bandwidth'],h['uses'],h['status'],h['company'],h['os'],h['other'],h['jointime'],h['modifytime'],h['modifyman'])
			description = u"<b>主机标识：</b>%s<br><b>地址：</b>%s/%s/%s<br><b>用途：</b>%s" % (h['hostname'],h['addr1_ip'],h['addr2_ip'],h['addr3_ip'],h['uses'])
			delman = web.ctx.session.username
			deltime = int(time.time())
			models.addHistory(content,description,delman,deltime)

			models.delHost(hid)
			raise web.seeother('/main')
		else:
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
	
	def POST(self):
		hid = web.input().hid
		hostname = web.input().hostname.strip()
		city = web.input().city
		project = web.input().project
		idc = web.input().idc
		port = web.input().port.strip()
		addr1_ip = web.input().addr1_ip.strip()
		addr1_netmask = web.input().addr1_netmask.strip()
		addr1_gateway = web.input().addr1_gateway.strip()
		addr1_line = web.input().addr1_line.strip()
		addr2_ip = web.input().addr2_ip.strip()
		addr2_netmask = web.input().addr2_netmask.strip()
		addr2_gateway = web.input().addr2_gateway.strip()
		addr2_line = web.input().addr2_line.strip()
		addr3_ip = web.input().addr3_ip.strip()
		addr3_netmask = web.input().addr3_netmask.strip()
		addr3_gateway = web.input().addr3_gateway.strip()
		addr3_line = web.input().addr3_line.strip()
		memory = web.input().memory.strip()
		cpu = web.input().cpu.strip()
		disk = web.input().disk.strip()
		buytime = web.input().buytime
		servicetime = web.input().servicetime
		hardwareinfo = web.input().hardwareinfo
		bandwidth = web.input().bandwidth.strip()
		uses = web.input().uses.strip()
		status = web.input().status
		company = web.input().company.strip()
		os = web.input().os.strip()
		other = web.input().other

		# Input check
		if port != '':	
			if not base.checkPort(port):
				return base.code("<script language='javascript'>alert('端口不合法 !');window.history.back(-1);</script>")
	
		for ip in addr1_ip,addr1_gateway,addr2_ip,addr2_gateway,addr3_ip,addr3_gateway:
			if ip != '':
				if not base.checkIp(ip):
					return base.code("<script language='javascript'>alert('IP地址不合法，请检查 !');window.history.back(-1);</script>")
		for i in cpu,memory,disk:
			if i != '':
				if not base.isInt(i):
					return base.code("<script language='javascript'>alert('CPU/MEMORY/DISK 不合法，请检查 !');window.history.back(-1);</script>")

		result = models.modifyHost(hid,hostname,city,project,idc,port,addr1_ip,addr1_netmask,addr1_gateway,addr1_line,addr2_ip,addr2_netmask,addr2_gateway,addr2_line,addr3_ip,addr3_netmask,addr3_gateway,addr3_line,memory,cpu,disk,buytime,servicetime,hardwareinfo,bandwidth,uses,status,company,os,other,int(time.time()),web.ctx.session.username)
		if result:
			raise web.seeother('/main')
		else:
			return base.code("<script language='javascript'>alert('失败，该主机标识已存在!');window.history.back(-1);</script>")
			
class ModifyCity:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')

		input = web.input()
		if not input.cid.isdigit():
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
			
		if not input: raise web.seeother('/citylist') 
		if input.action == 'mc':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")
			city_info = models.getOneCity(input.cid)
			return render.modify_city(city_info[0])

		elif input.action == 'vc':
			city_info = models.getOneCity(input.cid)
			return render.view_city(city_info[0])
				
		elif input.action == 'dc':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")
			
			# Save to history
			c = models.getOneCity(input.cid)[0]
			content = "INSERT INTO city VALUE (%s, '%s', '%s')" % (c['cid'], c['city'], c['other'])
			description = u"<b>城市：</b>"+ c['city']
			delman = web.ctx.session.username
			deltime = int(time.time())
			models.addHistory(content,description,delman,deltime)

			models.delCity(input.cid)
			raise web.seeother('/citylist')
		else:
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")

	def POST(self):
		input = web.input()	
		result = models.modifyCity(input.cid, input.city.strip(), input.other)
		if result:
			raise web.seeother('/citylist')
		else:
			return base.code("<script language='javascript'>alert('失败，该城市已存在 !');window.history.back(-1);</script>")
			
class CityList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		city_host_count = []
		city_list = models.getCityInfo();
		#return city_list[0]
		one_count = []
		for c in city_list:
			host_count = models.getHostCountByCity(c.cid)	
			idc_count = models.getIDCCountByCity(c.cid)
			one_count.append(c.cid)
			one_count.append(c.city)
			one_count.append(idc_count)
			one_count.append(host_count)
			city_host_count.append(one_count)
			one_count = []
			
		if web.ctx.session.privilege == 0:
			return render.city_list(city_host_count)
		else:
			return render.city_list_admin(city_host_count)
		
class IDCList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		idc_info_list = []
		all_idc_list = models.getIDCInfo()
		cid_to_city = base.cidToCity()

		#[iid,city,idcname,hostcountbyidc,hztime,contact,fun],
		one_count = []
		for i in all_idc_list:
			city = base.getCity(i.city)
			host_count = models.getHostCountByIDC(i.iid)
			one_count.append(i.iid)
			one_count.append(city)
			one_count.append(i.idcname)
			one_count.append(host_count)
			one_count.append(i.hztime)
			one_count.append(i.contact)
			idc_info_list.append(one_count)
			one_count = []
				
		if web.ctx.session.privilege == 0:
			return render.idc_list(idc_info_list)
		else:
			return render.idc_list_admin(idc_info_list)

class ProjectList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		project_info_list = []
		all_project_list = models.getProjectInfo();
		one_count = []
	
		#[pid,project,idc,hostcount]
		for p in all_project_list:
			host_count = models.getHostCountByProject(p.pid)
			idc_count = models.getIDCCountByProject(p.pid)
			one_count.append(p.pid)
			one_count.append(p.project)
			one_count.append(idc_count)
			one_count.append(host_count)
			project_info_list.append(one_count)
			one_count = []
		
		if web.ctx.session.privilege == 0:
			return render.project_list(project_info_list)
		else:
			return render.project_list_admin(project_info_list)
	
class ModifyProject:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')

		input = web.input()
		if not input.pid.isdigit():
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
			
		if not input:
			raise web.seeother('/projectlist')

		if input.action == 'mp':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，决绝访问 !');window.history.back(-1);</script>")
			project_info = models.getOneProject(input.pid)
			return render.modify_project(project_info)

		elif input.action == 'vp':
			project_info = models.getOneProject(input.pid)
			return render.view_project(project_info)
				
		elif input.action == 'dp':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，决绝访问 !');window.history.back(-1);</script>")

			# Save to history
			p = models.getOneProject(input.pid)
			content = "INSERT INTO project VALUE (%s, '%s', '%s')" % (p['pid'], p['project'], p['other'])
			description = u"<b>项目：</b>"+ p['project']
			delman = web.ctx.session.username
			deltime = int(time.time())
			models.addHistory(content,description,delman,deltime)
			
			models.delProject(input.pid)
			raise web.seeother('/projectlist')
		else:
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")

	def POST(self):
		input = web.input()	
		result = models.modifyProject(input.pid, input.project.strip(), input.other)
		if result:
			raise web.seeother('/projectlist')
		else:
			return base.code("<script language='javascript'>alert('失败，该项目名称已存在 !');window.history.back(-1);</script>")
			
class CityList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		city_host_count = []
		city_list = models.getCityInfo();
		#return city_list[0]
		one_count = []
		for c in city_list:
			host_count = models.getHostCountByCity(c.cid)	
			idc_count = models.getIDCCountByCity(c.cid)
			one_count.append(c.cid)
			one_count.append(c.city)
			one_count.append(idc_count)
			one_count.append(host_count)
			city_host_count.append(one_count)
			one_count = []
			
		if web.ctx.session.privilege == 0:
			return render.city_list(city_host_count)
		else:
			return render.city_list_admin(city_host_count)
		
class ModifyIDC:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')

		input = web.input()
		if not input.iid.isdigit():
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
		if not input:
			raise web.seeother('/idclist')
		
		if input.action == 'mi':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，决绝访问 !');window.history.back(-1);</script>")
			idc = models.getOneIDC(input.iid)
			city_list = models.getCityInfo()
			return render.modify_idc(idc[0], city_list)

		elif input.action == 'vi':
			idc = models.getOneIDC(input.iid)
			city_list = models.getCityInfo()
			return render.view_idc(idc[0], city_list)
		
		elif input.action == 'di':
			if web.ctx.session.privilege == 0:
				return base.code("<script language='javascript'>alert('您没有足够的权限，决绝访问 !');window.history.back(-1);</script>")
			
			# Save to history
			i = models.getOneIDC(input.iid)[0]
			content = "INSERT INTO idc VALUE (%s,%s,'%s','%s',%s,'%s')" % (i['iid'], i['city'],i['idcname'],i['contact'],i['hztime'], i['other'])
			description = u"<b>IDC：</b>%s<br><b>备注：</b>%s" % (i['idcname'],i['other'])
			delman = web.ctx.session.username
			deltime = int(time.time())
			models.addHistory(content,description,delman,deltime)

			models.delIDC(input.iid)
			raise web.seeother('/idclist')
		else:
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")

	def POST(self):
		input = web.input()	
		result = models.modifyIDC(input.iid, input.idcname.strip(), input.city, input.contact.strip(), input.hztime, input.other)
		if result:
			raise web.seeother('/idclist')
		else:
			return base.code("<script language='javascript'>alert('失败，该IDC已存在 !');window.history.back(-1);</script>")

class CityListHost:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		else:
			input = web.input(city=None,idc=None,hc=None,page=None)
			if not input.city.isdigit() or not input.hc.isdigit():
				return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
			city = int(input.city)
			 	
			# Paging
			sysconf = models.getConfig()
			pagesize = sysconf['page']  # page_per_rows
			hostcount = int(input.hc)
			pages = int(hostcount / pagesize)	# page_count

			if (hostcount % pagesize):
				pages += 1				#page_count

			if input.page:
				if not input.page.isdigit():
					return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
				page = int(input.page)
			else:
				page = 1

			offset = pagesize * (page - 1)  # offset
			pagerows = models.getPageByCity(city, offset, pagesize)

			newhosts=[]
			for h in pagerows:
				h['project'] = base.getProject(h['project'])
				h['city'] = base.getCity(h['city'])
				h['idc'] = base.getIDC(h['idc'])
				h['status'] = base.getStatus(h['status'])
				newhosts.append(h)

			#page Nav
			if hostcount <= pagesize:
				page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
			elif page == 1:
				page_nav = u"<a href='/citylisthost?city=%d&hc=%d&page=%d'>下一页</a> | <a href='/citylisthost?city=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (city,hostcount,page+1,city,hostcount,pages,page,pages,hostcount)
			elif page == pages:
				page_nav = u"<a href='/citylisthost?city=%d&hc=%d&page=%d'>上一页</a> | <a href='/citylisthost?city=%d&hc=%d&page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (city,hostcount,page-1,city,hostcount,page,pages,hostcount)
			else:
				page_nav = u"<a href='/citylisthost?city=%d&hc=%d&page=%d'>下一页</a> | <a href='/citylisthost?city=%d&hc=%d&page=%d'>上一页</a> | <a href='/citylisthost?city=%d&hc=%d&page=1'>首页</a> | <a href='/citylisthost?city=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (city,hostcount,page+1,city,hostcount,page-1,city,hostcount,city,hostcount,pages,page,pages,hostcount)
				
			if web.ctx.session.privilege == 0:
				return render.city_list_host(newhosts,pages,page,page_nav)
			else:
				return render.city_list_host_admin(newhosts,pages,page,page_nav)

class IDCListHost:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		else:
			input = web.input(city=None,idc=None,hc=None,page=None)
			if not input.idc.isdigit() or not input.hc.isdigit():
				return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
			idc = int(input.idc)
			 	
			# Paging
			sysconf = models.getConfig()
			pagesize = sysconf['page']  # page_per_rows
			hostcount = int(input.hc)
			pages = int(hostcount / pagesize)	# page_count

			if (hostcount % pagesize):
				pages += 1				#page_count

			if input.page:
				if not input.page.isdigit():
					return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
				page = int(input.page)
			else:
				page = 1

			offset = pagesize * (page - 1)  # offset
			pagerows = models.getPageByIDC(idc, offset, pagesize)

			newhosts=[]
			for h in pagerows:
				h['project'] = base.getProject(h['project'])
				h['city'] = base.getCity(h['city'])
				h['idc'] = base.getIDC(h['idc'])
				h['status'] = base.getStatus(h['status'])
				newhosts.append(h)

			#page Nav
			if hostcount <= pagesize:
				page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
			elif page == 1:
				page_nav = u"<a href='/idclisthost?idc=%d&hc=%d&page=%d'>下一页</a> | <a href='/idclisthost?idc=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (idc,hostcount,page+1,idc,hostcount,pages,page,pages,hostcount)
			elif page == pages:
				page_nav = u"<a href='/idclisthost?idc=%d&hc=%d&page=%d'>上一页</a> | <a href='/idclisthost?idc=%d&hc=%d&page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (idc,hostcount,page-1,idc,hostcount,page,pages,hostcount)
			else:
				page_nav = u"<a href='/idclisthost?idc=%d&hc=%d&page=%d'>下一页</a> | <a href='/idclisthost?idc=%d&hc=%d&page=%d'>上一页</a> | <a href='/idclisthost?idc=%d&hc=%d&page=1'>首页</a> | <a href='/idclisthost?idc=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (idc,hostcount,page+1,idc,hostcount,page-1,idc,hostcount,idc,hostcount,pages,page,pages,hostcount)
				
			if web.ctx.session.privilege == 0:
				return render.idc_list_host(newhosts,pages,page,page_nav)
			else:
				return render.idc_list_host_admin(newhosts,pages,page,page_nav)

class ProjectListHost:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		else:
			input = web.input(project=None,idc=None,hc=None,page=None)
			if not input.project.isdigit() or not input.hc.isdigit():
				return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
			project = int(input.project)
			 	
			# Paging
			sysconf = models.getConfig()
			pagesize = sysconf['page']  # page_per_rows
			hostcount = int(input.hc)
			pages = int(hostcount / pagesize)	# page_count

			if (hostcount % pagesize):
				pages += 1				#page_count

			if input.page:
				if not input.project.isdigit():
					return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
				page = int(input.page)
			else:
				page = 1

			offset = pagesize * (page - 1)  # offset
			pagerows = models.getPageByProject(project, offset, pagesize)

			newhosts=[]
			for h in pagerows:
				h['project'] = base.getProject(h['project'])
				h['city'] = base.getCity(h['city'])
				h['idc'] = base.getIDC(h['idc'])
				h['status'] = base.getStatus(h['status'])
				newhosts.append(h)

			#page Nav
			if hostcount <= pagesize:
				page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
			elif page == 1:
				page_nav = u"<a href='/projectlisthost?project=%d&hc=%d&page=%d'>下一页</a> | <a href='/projectlisthost?project=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (project,hostcount,page+1,project,hostcount,pages,page,pages,hostcount)
			elif page == pages:
				page_nav = u"<a href='/projectlisthost?project=%d&hc=%d&page=%d'>上一页</a> | <a href='/projectlisthost?project=%d&hc=%d&page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (project,hostcount,page-1,project,hostcount,page,pages,hostcount)
			else:
				page_nav = u"<a href='/projectlisthost?project=%d&hc=%d&page=%d'>下一页</a> | <a href='/projectlisthost?project=%d&hc=%d&page=%d'>上一页</a> | <a href='/projectlisthost?project=%d&hc=%d&page=1'>首页</a> | <a href='/projectlisthost?project=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (project,hostcount,page+1,project,hostcount,page-1,project,hostcount,project,hostcount,pages,page,pages,hostcount)
				
			if web.ctx.session.privilege == 0:
				return render.project_host_list(newhosts,pages,page,page_nav)
			else:
				return render.project_host_list_admin(newhosts,pages,page,page_nav)

class ProjectIDCList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		
		if not web.input():
			raise web.seeother('/projectlist')

		if not web.input().project.isdigit():
			return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")

		pid = int(web.input().project)
		idc_dict = models.getIDCInfoByProject(pid)
		projects_dict = base.pidToProject()

		# Get idc list by project id
		project_idc_list = []
		#{pid,iid,idcname,hostcount by pid and iid}
		one_idc_dict = {}
		for i in idc_dict:
			iid = i['idc']
			idc_info = models.getOneIDC(iid)
			if not idc_info:
				idc_info.idcname = 'Unknown'
			else:
				idc_info = idc_info[0]
				
			hostcount = models.getHostCountByPidAndIid(pid,iid)

			one_idc_dict['pid'] = pid
			one_idc_dict['iid'] = iid
			one_idc_dict['idcname'] = idc_info.idcname
			one_idc_dict['hostcount'] = hostcount
			project_idc_list.append(one_idc_dict)
			one_idc_dict = {}

		return render.project_idc_list(project_idc_list, projects_dict[pid])

class ProjectIDCHostList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		else:
			input = web.input(pid=None,iid=None,hc=None,page=None)
			if not input.pid.isdigit() or not input.iid.isdigit():
				return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")
			pid = int(input.pid)
			iid = int(input.iid)
			 	
			# Paging
			sysconf = models.getConfig()
			pagesize = sysconf['page']  # page_per_rows
			hostcount = int(input.hc)
			pages = int(hostcount / pagesize)	# page_count

			if (hostcount % pagesize):
				pages += 1				#page_count

			if input.page:
				page = int(input.page)
			else:
				page = 1

			offset = pagesize * (page - 1)  # offset
			pagerows = models.getPageByPidAndIid(pid,iid,offset,pagesize)

			newhosts=[]
			for h in pagerows:
				h['project'] = base.getProject(h['project'])
				h['city'] = base.getCity(h['city'])
				h['idc'] = base.getIDC(h['idc'])
				h['status'] = base.getStatus(h['status'])
				newhosts.append(h)

			#page Nav
			if hostcount <= pagesize:
				page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
			elif page == 1:
				page_nav = u"<a href='/pihl?pid=%d&iid=%d&hc=%d&page=%d'>下一页</a> | <a href='/pihl?pid=%d&iid=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (pid,iid,hostcount,page+1,pid,iid,hostcount,pages,page,pages,hostcount)
			elif page == pages:
				page_nav = u"<a href='/pihl?pid=%d&iid=%d&hc=%d&page=%d'>上一页</a> | <a href='/pihl?pid=%d&iid=%d&hc=%d&page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (pid,iid,hostcount,page-1,pid,iid,hostcount,page,pages,hostcount)
			else:
				page_nav = u"<a href='/pihl?pid=%d&iid=%d&hc=%d&page=%d'>下一页</a> | <a href='/pihl?pid=%d&iid=%d&hc=%d&page=%d'>上一页</a> | <a href='/pihl?pid=%d&iid=%d&hc=%d&page=1'>首页</a> | <a href='/pihl?pid=%d&iid=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (pid,iid,hostcount,page+1,pid,iid,hostcount,page-1,pid,iid,hostcount,pid,iid,hostcount,pages,page,pages,hostcount)
				
			if web.ctx.session.privilege == 0:
				return render.project_idc_host_list(newhosts,pages,page,page_nav)
			else:
				return render.project_idc_host_list_admin(newhosts,pages,page,page_nav)

class CityIDCList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		
		if not web.input():
			raise web.seeother('/projectlist')
		cid = int(web.input().city)
		idc_dict = models.getIDCInfoByCity(cid)
		citys_dict = base.cidToCity()

		city_idc_list = []
		#{cid,iid,idcname,hostcount by cid and iid}
		one_idc_dict = {}
		for i in idc_dict:
			hostcount = models.getHostCountByCidAndIid(cid,i.iid)

			one_idc_dict['cid'] = cid
			one_idc_dict['iid'] = i.iid
			one_idc_dict['idcname'] = i.idcname
			one_idc_dict['hostcount'] = hostcount
			city_idc_list.append(one_idc_dict)
			one_idc_dict = {}

		return render.city_idc_list(city_idc_list, citys_dict[cid])

class CityIDCHostList:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		else:
			input = web.input(cid=None,iid=None,hc=None,page=None)
			cid = int(input.cid)
			iid = int(input.iid)
			 	
			# Paging
			sysconf = models.getConfig()
			pagesize = sysconf['page']  # page_per_rows
			hostcount = int(input.hc)
			pages = int(hostcount / pagesize)	# page_count

			if (hostcount % pagesize):
				pages += 1				#page_count

			if input.page:
				page = int(input.page)
			else:
				page = 1

			offset = pagesize * (page - 1)  # offset
			pagerows = models.getPageByIDC(iid,offset,pagesize)

			newhosts=[]
			for h in pagerows:
				h['project'] = base.getProject(h['project'])
				h['city'] = base.getCity(h['city'])
				h['idc'] = base.getIDC(h['idc'])
				h['status'] = base.getStatus(h['status'])
				newhosts.append(h)

			#page Nav
			if hostcount <= pagesize:
				page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
			elif page == 1:
				page_nav = u"<a href='/cihl?cid=%d&iid=%d&hc=%d&page=%d'>下一页</a> | <a href='/cihl?cid=%d&iid=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (cid,iid,hostcount,page+1,cid,iid,hostcount,pages,page,pages,hostcount)
			elif page == pages:
				page_nav = u"<a href='/cihl?cid=%d&iid=%d&hc=%d&page=%d'>上一页</a> | <a href='/cihl?cid=%d&iid=%d&hc=%d&page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (cid,iid,hostcount,page-1,cid,iid,hostcount,page,pages,hostcount)
			else:
				page_nav = u"<a href='/cihl?cid=%d&iid=%d&hc=%d&page=%d'>下一页</a> | <a href='/cihl?cid=%d&iid=%d&hc=%d&page=%d'>上一页</a> | <a href='/cihl?cid=%d&iid=%d&hc=%d&page=1'>首页</a> | <a href='/cihl?cid=%d&iid=%d&hc=%d&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (cid,iid,hostcount,page+1,cid,iid,hostcount,page-1,cid,iid,hostcount,cid,iid,hostcount,pages,page,pages,hostcount)
				
			if web.ctx.session.privilege == 0:
				return render.city_idc_host_list(newhosts,pages,page,page_nav)
			else:
				return render.city_idc_host_list_admin(newhosts,pages,page,page_nav)

class Index:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		conf = models.getConfig()
		sys_overview = models.getSysOverView()
		status_overview = models.getStatusOverView()
		
		return render.index(conf,sys_overview,status_overview)
	
	def POST(self):
		input = web.input()
		if input.name == '':
			return base.code("<script language='javascript'>alert('请输入站点名称 !');window.history.back(-1);</script>")
		elif not input.page.isdigit():
			return base.code("<script language='javascript'>alert('分页只能是数字 !');window.history.back(-1);</script>")
		else:
			models.updateConfig(input.name, int(input.page))
			raise web.seeother('/index')
			
class Search:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		
		input = web.input(page=None)	
		# Paging
		sysconf = models.getConfig()
		pagesize = sysconf['page']  # page_per_rows
		input.word = input.word.replace("'","\\'")
		
		if input.ops == '1':
			hostcount = models.getHostCountBySearch('hostname',input.word)
		elif input.ops == '2':
			hostcount = models.getHostCountBySearchIp(input.word)
		elif input.ops == '5':
			hostcount = models.getHostCountBySearch('port',input.word)
		elif input.ops == '6':
			hostcount = models.getHostCountBySearch('status',input.word)
		elif input.ops == '7':
			hostcount = models.getHostCountBySearch('bandwidth',input.word)
		elif input.ops == '8':
			hostcount = models.getHostCountBySearch('uses',input.word)
		elif input.ops == '9':
			hostcount = models.getHostCountBySearch('os',input.word)
		elif input.ops == '10':
			hostcount = models.getHostCountBySearch('company',input.word)
		elif input.ops == '11':
			hostcount = models.getHostCountBySearch('hardwareinfo',input.word)
		elif input.ops == '12':
			hostcount = models.getHostCountBySearch('other',input.word)
		elif input.ops == '13':
			hostcount = models.getHostCountBySearch('modifyman',input.word)
		
		pages = int(hostcount / pagesize)	# page_count

		if (hostcount % pagesize):
			pages += 1				#page_count

		if input.page:
			page = int(input.page)
		else:
			page = 1

		offset = pagesize * (page - 1)  # offset

		if input.ops == '1':
			pagerows = models.getPageBySearch('hostname',input.word,str(offset),str(pagesize))
		elif input.ops == '2':
			pagerows = models.getPageBySearchIp(input.word,str(offset),str(pagesize))
		elif input.ops == '5':
			pagerows = models.getPageBySearch('port',input.word,str(offset),str(pagesize))
		elif input.ops == '6':
			pagerows = models.getPageBySearch('status',input.word,str(offset),str(pagesize))
		elif input.ops == '7':
			pagerows = models.getPageBySearch('bandwidth',input.word,str(offset),str(pagesize))
		elif input.ops == '8':
			pagerows = models.getPageBySearch('uses',input.word,str(offset),str(pagesize))
		elif input.ops == '9':
			pagerows = models.getPageBySearch('os',input.word,str(offset),str(pagesize))
		elif input.ops == '10':
			pagerows = models.getPageBySearch('company',input.word,str(offset),str(pagesize))
		elif input.ops == '11':
			pagerows = models.getPageBySearch('hardwareinfo',input.word,str(offset),str(pagesize))
		elif input.ops == '12':
			pagerows = models.getPageBySearch('other',input.word,str(offset),str(pagesize))
		elif input.ops == '13':
			pagerows = models.getPageBySearch('modifyman',input.word,str(offset),str(pagesize))

		newhosts=[]
		for h in pagerows:
			h['project'] = base.getProject(h['project'])
			h['city'] = base.getCity(h['city'])
			h['idc'] = base.getIDC(h['idc'])
			h['status'] = base.getStatus(h['status'])
			newhosts.append(h)
		
		ops = int(input.ops)

		#page Nav
		if hostcount <= pagesize:
			page_nav = u"共 <b>%s</b> 条记录" % (hostcount)
		elif page == 1:
			page_nav = u"<a href='/search?ops=%d&word=%s&page=%d'>下一页</a> | <a href='/search?ops=%d&word=%s&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (ops,input.word,page+1,ops,input.word,pages,page,pages,hostcount)
		elif page == pages:
			page_nav = u"<a href='/search?ops=%d&word=%s&page=%d'>上一页</a> | <a href='/search?ops=%d&word=%s&page=1'>首页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (ops,input.word,page-1,ops,input.word,page,pages,hostcount)
		else:
			page_nav = u"<a href='/search?ops=%d&word=%s&page=%d'>下一页</a> | <a href='/search?ops=%d&word=%s&page=%d'>上一页</a> | <a href='/search?ops=%d&word=%s&page=1'>首页</a> | <a href='/search?ops=%d&word=%s&page=%d'>尾页</a> | (%d / %d) , 共 <b>%d</b> 条记录" % (ops,input.word,page+1,ops,input.word,page-1,ops,input.word,ops,input.word,pages,page,pages,hostcount)

		if web.ctx.session.privilege == 0:
			return render.main(newhosts,pages,page,page_nav)
		else:
			return render.main_admin(newhosts,pages,page,page_nav)
	
		if input.ops == '1':
			result = models.searchHostName(input.content)
			return result

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

		if web.ctx.session.privilege == 2:
			return  render.user_list_admin(user_info_list)
		else:
			return  render.user_list(user_info_list)
		
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

		# User is not admin
		else:
			if input.oldpassword != '':
				if input.password == '':
					return base.code("<script language='javascript'>alert('请输入一个新密码 !');window.history.back(-1);</script>")
				if input.password2 != input.password:
					return base.code("<script language='javascript'>alert('密码不匹配 !');window.history.back(-1);</script>")
			
				# Get password in database	
				user_info = models.getUserInfo(web.ctx.session.username)
				db_pwd = user_info['password']
				old_pwd = hashlib.new('md5', input.oldpassword+'Steven').hexdigest()
				if db_pwd != old_pwd:
					return base.code("<script language='javascript'>alert('原密码输入错误 !');window.history.back(-1);</script>")
				else:
					new_pwd = hashlib.new('md5', input.password+'Steven').hexdigest()
					models.ChangeUserPWD(web.ctx.session.username,new_pwd)
		
			models.UpdateUserInfo(web.ctx.session.username,input.phone.strip(),input.email.strip(),input.other)
			raise web.seeother('/userlist')

class Export:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		if web.ctx.session.privilege != 2:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")

		all_hosts = models.getAllHosts()
		new_hosts=[]
		for h in all_hosts:
			h['project'] = base.getProject(h['project'])
			h['city'] = base.getCity(h['city'])
			h['idc'] = base.getIDC(h['idc'])
			h['status'] = base.getStatus(h['status'])
			new_hosts.append(h)
		
		# Export host data
		wbk = xlwt.Workbook(encoding='utf-8')
		style = xlwt.XFStyle()
		style2 = xlwt.XFStyle()
		font = xlwt.Font()
		font2 = xlwt.Font()
		font2.bold = True
		font.name = 'SimSum'
		style.alignment.wrap=1
		style.font = font
		style2.font = font2
		sheet = wbk.add_sheet('hosts')
		
		# Define excel header names
		sheet.write(0,0,'主机标识', style2)
		sheet.write(0,1,'所属项目', style2)
		sheet.write(0,2,'所在城市', style2)
		sheet.write(0,3,'所在IDC', style2)
		sheet.write(0,4,'地址一', style2)
		sheet.write(0,5,'地址二', style2)
		sheet.write(0,6,'地址三', style2)
		sheet.write(0,7,'登录端口', style2)
		sheet.write(0,8,'所属公司', style2)
		sheet.write(0,9,'带宽', style2)
		sheet.write(0,10,'用途', style2)
		sheet.write(0,11,'状态', style2)
		sheet.write(0,12,'操作系统', style2)
		sheet.write(0,13,'内存(GB)', style2)
		sheet.write(0,14,'CPU(核心)', style2)
		sheet.write(0,15,'磁盘(GB)', style2)
		sheet.write(0,16,'购买时间', style2)
		sheet.write(0,17,'质保时间', style2)
		sheet.write(0,18,'硬件详细信息', style2)
		sheet.write(0,19,'备注', style2)

		# Start export
		row = 1
		for  i in new_hosts:
			sheet.write(row,0,i['hostname'])
			sheet.write(row,1,i['project'])
			sheet.write(row,2,i['city'])
			sheet.write(row,3,i['idc'])
			sheet.col(4).width = 0x0d00 + 3000
			sheet.col(5).width = 0x0d00 + 3000
			sheet.col(6).width = 0x0d00 + 3000
			sheet.write(row,4,'IP:'+i['addr1_ip']+'\nNETMASK:'+i['addr1_netmask']+'\nGATEWAY:'+i['addr1_gateway']+'\nLINE:'+i['addr1_line'], style)
			sheet.write(row,5,'IP:'+i['addr2_ip']+'\nNETMASK:'+i['addr2_netmask']+'\nGATEWAY:'+i['addr2_gateway']+'\nLINE:'+i['addr2_line'], style)
			sheet.write(row,6,'IP:'+i['addr3_ip']+'\nNETMASK:'+i['addr3_netmask']+'\nGATEWAY:'+i['addr3_gateway']+'\nLINE:'+i['addr3_line'], style)
			sheet.write(row,7,i['port'])
			sheet.write(row,8,i['company'])
			sheet.write(row,9,i['bandwidth'])
			sheet.write(row,10,i['uses'])
			sheet.write(row,11,i['status'])
			sheet.write(row,12,i['os'])
			sheet.write(row,13,i['memory'])
			sheet.write(row,14,i['cpu'])
			sheet.write(row,15,i['disk'])
			sheet.write(row,16,i['buytime'])
			sheet.write(row,17,i['servicetime'])
			sheet.write(row,18,i['hardwareinfo'])
			sheet.write(row,19,i['other'])
			row += 1
	
		wbk.save('download/hosts.xls')
		file = 'hosts.xls'
		return base.DownLoad(file)
		
class Error404:
	def GET(self):
		return render_plain.page404()

class Error500:
	def GET(self):
		return render_plain.page500()

class History:
	def GET(self):
		if not base.logged():
			raise web.seeother('/')
		if web.ctx.session.privilege == 0:
			return base.code("<script language='javascript'>alert('您没有足够的权限，拒绝访问 !');window.history.back(-1);</script>")
		history = models.getHistory()		
		history = list(history)		
		for h in history:
			ltime = time.localtime(int(h['deltime']))
			deltime = time.strftime("%Y-%m-%d %H:%M:%S",ltime)
			h['deltime'] = deltime
		
		input = web.input(action=None,hid=None)

		if not input.action:	
			return render.history(history)
		else:
			# Remove history
			if input.action == 'dh':
				models.delOneHistory(input.hid)
				raise web.seeother('/history')
			# Resotre history
			elif input.action == 'rh':
			 	if models.restoreHistory(input.hid):
					models.delOneHistory(input.hid)
					return base.code("<script language='javascript'>alert('恢复成功 !');window.location.href='/history'; </script>")
				else:
					return base.code("<script language='javascript'>alert('恢复失败，此记录可能已存在，请检查！');window.history.back(-1);</script>")
				
			else:
				return base.code("<script language='javascript'>alert('参数错误 !');window.history.back(-1);</script>")

		
