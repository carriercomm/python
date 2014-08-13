# -*- coding:utf8 -*-
import os
import sys
import paramiko
import Colorer
import logging  
import logging.config

from tornado import template
from config import *

#日志初始化  
LOG_FILENAME = 'log.conf'  
logging.config.fileConfig(LOG_FILENAME)  
logger = logging.getLogger("simple_log_example")
#----------------------------------------------------------------------------------------
#远程执行命令
def connect(server, port, username, password):
        logger.info("begin to connect the server: "+server)
        #keyfile = os.path.join(os.path.dirname(__file__), "keydir/id_rsa")
        keyfile = os.path.join(os.path.dirname(__file__), "keydir/"+username)
        global sshclient
        sshclient = paramiko.SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshclient.connect(server, port, username, password,key_filename=keyfile) 
        logger.info("success to connect the server: "+server)
        #return sshclient

def execute(commands):
	ret_value = []
	for cmd in commands:
		stdin, stdout, stderr = sshclient.exec_command("sudo "+cmd)
		exit_code = stdout.channel.recv_exit_status()
                if exit_code != 0:
                    logger.error(cmd)
                else:
                   logger.info(cmd)
		ret_value.append((exit_code, stderr.readlines(), stdout.readlines()))
	return ret_value

def finish():
    sshclient.close()
    logger.info("close the ssh connect.")
#----------------------------------------------------------------------------------------
#上传文件
def upload(server, port, username, password, localfile, remotefile):
	t = paramiko.Transport((server, port))
	t.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(t)
	remotepath = remotefile
	localpath = localfile
	ret = sftp.put(localpath, remotepath)
	t.close()
	return ret


#----------------------------------------------------------------------------------------
#下载文件
def download(server, port, username, password, remotefile, localfile):
	t = paramiko.Transport((server, port))
	t.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(t)
	remotepath = remotefile
	localpath = localfile
	ret = sftp.get(remotepath, localpath)
	t.close()
	return ret

#----------------------------------------------------------------------------------------
#根据模板生成配置文件(字符串)
def genconfigstring(configtemplate, configvalues = {}):
	global template_path
	loader = template.Loader(template_path)
	ret = loader.load(configtemplate).generate(**configvalues)
	return ret

#----------------------------------------------------------------------------------------
#根据模板生成配置文件(文本文件)
def genconfigfile(configfile, configtemplate, configvalues = {}):
	fp_config = open(configfile, 'w')
	configstring = genconfigstring(configtemplate, configvalues)
	fp_config.write(configstring )
	fp_config.close()
	return configstring

