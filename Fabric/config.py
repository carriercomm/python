#!/usr/bin/env python
# coding=utf-8
import ConfigParser

config = ConfigParser.ConfigParser()

class Get_data:
	def __init__(self,ini_file):
		self.ini_file = ini_file
		config.read(ini_file)
	
	def Show_section(self):
		self.section = config.sections()
		print self.section
		return self.section
	
	def Show_option(self,section):
		self.option = config.options(section)
		print self.option
		return self.option
		
	def Show_option_data(self,section,option):
		self.option_data = config.get(section,option)
		print self.option_data
		return self.option_data
		
	def Show_section_data(self,section):
		host_list = []
		option_list = config.options(section)
		for i in option_list:
			ip = config.get(section,i)
			host_list.append(ip)
		print host_list
		return host_list
		
	def Show_all_data(self):
		all_host_list = []
		section_list = config.sections()
		for i in section_list:
			option_list = config.options(i)
			for j in option_list:
				ip = config.get(i,j)
				all_host_list.append(ip)
		print all_host_list
		return all_host_list
		
'''
if __name__ == "__main__":
	getdata = Get_data('./hosts.ini')
	#getdata.Show_section()
	#getdata.Show_option('web-host')
	#getdata.Show_option_data('web-host','node1')
	#getdata.Show_section_data('web-host')
	getdata.Show_all_data()
'''
if __name__ == "__main__":
	getdata = Get_data('./hosts.ini')
	getdata.Show_section()
	getdata.Show_option('web-host')
	getdata.Show_option_data('web-host','node2')
	getdata.Show_section_data('web-host')
	#data = getdata.Show_all_data()
        #print data
