#!/usr/local/python2.7.3/bin/python
#-*- coding:utf-8 -*-
__author__ = 'liangsh'

import sys
import os
import re
import time
import datetime
import MySQLdb
import logging
from logging.handlers import RotatingFileHandler
reload(sys)
sys.setdefaultencoding('utf8')
import smtplib
from email.mime.text import MIMEText
from email.Header import Header

####
mailto_list=['hongyh@baoxian.com','liangsh@baoxian.com']
mail_host="smtp.qq.com"
mail_port='465'
mail_user="476818061"
mail_pass="suker41341"
mail_postfix="qq.com"
mail_subject='一区业务库备份报告-'+str(datetime.date.today().strftime('%Y%m%d'))
####
mysql_data_save_date = 90
local_file_save_date = 5
backup_dir = '/data/backup_mysql_biz1/'
log_dir = '/data/log/dataclear/'
####
src_dbhost = '192.168.100.228'
src_database = 'b2b_biz1'
src_user = 'dataclear'
src_passwd = 'Iu:*H?O#'
####
dest_dbhost = 'localhost'
dest_database = 'b2b_biz1'
dest_user = 'root'
dest_passwd = 'IuB1$RB'
####
table_list = ('verify_task','ins_multi_quote','vehicle_enquiry','quote_task','insure_task','edi_task','order_item_info','order_info','order_delivery_info','order_payment_info','order_remarks','order_searchable_field','order_ext_info','insurance_application','insurance_policy','quote_task_history','vehicle_enquiry_temp','insure_task_history')
####
local_backup_content = {}
remote_backup_content = {}
delete_data_content = {}
#create logger
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
#create formatter
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s - %(message)s")
#create console handler and set level to debug
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
#create Rotating file handler and set level to debug
Rthandler = RotatingFileHandler(log_dir+'biz1.log', maxBytes=10*1024*1024,backupCount=10)
Rthandler.setFormatter(formatter)
#add formatter to console and Rthandler
console.setFormatter(formatter)
Rthandler.setFormatter(formatter)
#add console and Rthandler to logger
#logger.addHandler(console)
logger.addHandler(Rthandler)


class DataClear(object):
        """docstring for DataClear"""
        l_conn = None
        r_conn = None
        l_cursor = None
        r_cursor = None
        num_multi_id = 0
        num_enquiry_id = 0
        def __init__(self):
            for filename in os.listdir(backup_dir):
                if re.search((datetime.date.today()+datetime.timedelta(days=-local_file_save_date)).strftime('%Y%m%d'), filename):
                    logger.info('begin to delete '+str(local_file_save_date)+' days ago local backup file: '+os.path.join(backup_dir,filename)+'.')
                    os.remove(os.path.join(backup_dir,filename))
            logger.info('end of delete '+str(local_file_save_date)+' days ago local backup file.')

        def connect(self,db_host='src'):
            """
            build a connect method
            """
            try:
                if db_host == 'dest':
                		self.r_conn = MySQLdb.connect(host=dest_dbhost,user=dest_user,passwd=dest_passwd,db=dest_database)
                		logger.info('connect to dest database '+dest_database+' of '+dest_dbhost+' with user '+dest_user+' success.')
                else:
                		self.l_conn = MySQLdb.connect(host=src_dbhost,user=src_user,passwd=src_passwd,db=src_database)
                		logger.info('connect to src database '+src_database+' of '+src_dbhost+' with user '+src_user+' success.')
            except Exception, e:
                raise
                logger.error('connect to '+db_host+' database host error!')
                sys.exit(1)

        def execute(self,sql,db_host='src'):
            """
            execute sql
            """
            try:
                if db_host == 'dest':
                    #self.connect(db_host)
                    self.r_cursor = self.r_conn.cursor()
                    self.line = self.r_cursor.execute(sql)
                    return (self.line,self.r_cursor)
                else:
                    #self.connect(db_host)
                    self.l_cursor = self.l_conn.cursor()
                    self.line = self.l_cursor.execute(sql)
                    return (self.line,self.l_cursor)
            except(AttributeError, MySQLdb.OperationalError):
                logger.warning(db_host+' mysql is go away ,reconnect!')
                if db_host == 'dest':
                    self.connect(db_host)
                    self.r_cursor = self.r_conn.cursor()
                    self.line = self.r_cursor.execute(sql)
                    return (self.line,self.r_cursor)
                else:
                    self.connect(db_host)
                    self.l_cursor = self.l_conn.cursor()
                    self.line = self.l_cursor.execute(sql)
                    return (self.line,self.l_cursor)
      
        def get_multi_id(self):
            """
            get multi id
            """
            self.multi_id_list = [ ]
            self.in_m_id_sql = ''
            try:
                multi_id_file = backup_dir+'multi_id_file_'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                multi_f = open(multi_id_file,'w')
                logger.info('open file '+multi_id_file+' for write success.')
                logger.info('begin to search multi id by save time.')
                cur = self.execute("select id from ins_multi_quote where date_created < '"+(datetime.date.today()+datetime.timedelta(days=-mysql_data_save_date)).strftime('%Y-%m-%d')+' 00:00:00'+"'")
                #cursor = self.execute("select id from ins_multi_quote where date_created < '"+(datetime.date.today()+datetime.timedelta(days=-mysql_data_save_date)).strftime('%Y-%m-%d')+' 00:00:00'+"'"+" limit 100")
                results = cur[1].fetchall()
                self.num_multi_id = len(results)
                logger.info('End search, total number of multi_id is: '+str(self.num_multi_id)+'.')  
                if self.num_multi_id == 0:
                    logger.warning('multi_id is 0,exit.')
                    sys.exit(1)
                for r in results:
                    multi_f.write(r[0]+'\n')
                    self.multi_id_list.append(r[0])
                logger.info('total multi_id is writed into file: '+multi_id_file+'.')
                multi_f.close()
                logger.info('close file '+multi_id_file+' success.')
                logger.info('begin to map multi id sql.')
                for m_id in self.multi_id_list:
                    self.in_m_id_sql = self.in_m_id_sql+"'"+m_id+"',"
                self.in_m_id_sql=self.in_m_id_sql.strip(",")
                logger.info('end of map multi id sql.')
            except Exception, e:
                raise
                sys.exit(1)

        def get_enquiry_id(self):
            """
            get enquiry id
            """
            self.enquiry_id_list = [ ]
            self.in_e_id_sql = ''
            try:
                enquiry_id_file = backup_dir+'enquiry_id_file_'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                enquiry_f = open(enquiry_id_file,'w')
                logger.info('open file '+enquiry_id_file+' for write success.')
                logger.info('begin to search enquiry id by multi id.')
                cur = self.execute('select id from vehicle_enquiry where multi_quote_id in ('+self.in_m_id_sql+')')
                results = cur[1].fetchall()
                self.num_enquiry_id = len(results)              
                logger.info('End search,total number of enquiry_id is: '+str(self.num_enquiry_id)+'.')
                for r in results:
                    enquiry_f.write(r[0]+'\n')
                    self.enquiry_id_list.append(r[0])
                logger.info('total enquiry_id is writed into file: '+enquiry_id_file+'.')
                enquiry_f.close()
                logger.info('close file '+enquiry_id_file+' success.')
                logger.info('begin to map enquiry id sql.')
                for e_id in self.enquiry_id_list:
                    self.in_e_id_sql = self.in_e_id_sql+"'"+e_id+"',"
                self.in_e_id_sql=self.in_e_id_sql.strip(",")
                logger.info('end of map enquiry id sql.')
            except Exception, e:
                raise
                sys.exit(1)

        def local_backup(self,table,wheresql,field='biz_transaction_id'):
            """
        	local backup data
        	"""
            try:
                self.table_file = backup_dir+table+'_'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                logger.info('begin to local backup table: '+table+'.')
                cur = self.execute("SELECT * INTO OUTFILE "+"'"+self.table_file+"'"+" FIELDS TERMINATED BY "+"','"+" OPTIONALLY ENCLOSED BY "+"'\"'"+" LINES TERMINATED BY "+"'\n'"+" FROM "+table+" WHERE "+field+" in ("+wheresql+")")
                logger.info('End of local backup table:'+table+' '+str(cur[0])+' line affect.')
                local_backup_content[table] = cur[0]
            except Exception, e:
                raise
                sys.exit(1)

        def remote_backup(self,database,table,table_file):
            """
        	remote backup data
        	"""
            try:
                logger.info('begin to remote backup table: '+database+'.'+table+'.')
                self.execute("SET FOREIGN_KEY_CHECKS=0","dest")
                cur = self.execute("LOAD DATA INFILE "+"'"+table_file+"'"+" INTO TABLE "+database+"."+table+" FIELDS TERMINATED BY "+"','"+" OPTIONALLY ENCLOSED BY "+"'\"'"+" LINES TERMINATED BY "+"'\\n'","dest")
                self.r_conn.commit()
                logger.info('End of remote backup table:'+database+'.'+table+' '+str(cur[0])+' line affect.')
                remote_backup_content[table] = cur[0]
            except Exception, e:
                raise
                sys.exit(1)
                
        def delete_data(self,table,wheresql,field='biz_transaction_id'):
            """
        	delete data
        	"""
            try:
                logger.info('begin to delete table: '+table+'.')
                self.execute("SET FOREIGN_KEY_CHECKS=0")
                cur = self.execute("DELETE FROM "+table+" WHERE "+field+" IN ("+wheresql+")")
                #self.execute("optimize table "+table)
                self.l_conn.commit()
                logger.info('End of delete table:'+table+' '+str(cur[0])+' line affect.')
                delete_data_content[table] = cur[0]
            except Exception, e:
                raise
                sys.exit(1)

        def send_mail(self,to_list,sub,content):
            if isinstance(content,unicode):
                content = str(content)
            me= ("%s<"+mail_user+"@"+mail_postfix+">") % (Header('_mailFrom管理员','utf-8'),)
            msg = MIMEText(content,_subtype='plain',_charset='utf-8')
            if not isinstance(sub,unicode):
                sub = unicode(sub)
            msg['Subject'] = sub
            msg['From'] = me
            msg['To'] = ";".join(to_list)
            msg["Accept-Language"]="zh-CN"
            msg["Accept-Charset"]="ISO-8859-1,utf-8"
            try:
                server = smtplib.SMTP_SSL(mail_host,mail_port)
                server.login(mail_user,mail_pass)
                server.sendmail(me,to_list,msg.as_string())
                server.close()
                return True
            except Exception, e:
                print str(e)
                return False

        def finish(self):
            """
        	finish
        	"""
            try:
                if(self.l_cursor):
                    self.l_cursor.close()
                    logger.info('finish, close the connect of '+src_dbhost+'.')
                if(self.r_cursor):
                    self.r_cursor.close()
                    logger.info('finish, close the connect of '+dest_dbhost+'.')
                if(self.l_conn):
                    self.l_conn.commit()
                    self.l_conn.close()
                if(self.r_conn):
                    self.r_conn.commit()
                    self.r_conn.close()
                logger.info('all finish,total number of multi_id is: '+str(self.num_multi_id)+' and'+' enquiry_id is: '+str(self.num_enquiry_id)+'.')
                #print self.l_cursor
                #print self.r_cursor
                #print self.l_conn
                #print self.r_conn
                
            except Exception, e:
                raise
                sys.exit(1)
                

if __name__=="__main__":
    todo = DataClear()
    todo.get_multi_id()
    todo.get_enquiry_id()
    for t in table_list:
        if t == 'ins_multi_quote':
            #pass
            todo.local_backup('ins_multi_quote',todo.in_m_id_sql,'id')
            todo.remote_backup(dest_database,t,todo.table_file)
        elif t == 'verify_task':
            #pass
            todo.local_backup('verify_task',todo.in_m_id_sql,'multi_quote_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data('verify_task',todo.in_m_id_sql,'multi_quote_id')
        elif t == 'vehicle_enquiry':
            #pass
            todo.local_backup('vehicle_enquiry',todo.in_e_id_sql,'id')
            todo.remote_backup(dest_database,t,todo.table_file)
        elif t == 'quote_task':
            #pass
            todo.local_backup('quote_task',todo.in_e_id_sql,'enquiry_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data('quote_task',todo.in_e_id_sql,'enquiry_id')
        elif t == 'insure_task':
            #pass 
            todo.local_backup('insure_task',todo.in_e_id_sql,'enquiry_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data('insure_task',todo.in_e_id_sql,'enquiry_id')
        elif t == 'edi_task':
            #pass  
            todo.local_backup('edi_task',todo.in_e_id_sql,'enquiry_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data('edi_task',todo.in_e_id_sql,'enquiry_id')
        elif t == 'quote_task_history':
            #pass  
            todo.local_backup(t,todo.in_e_id_sql,'enquiry_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data(t,todo.in_e_id_sql,'enquiry_id')
        elif t == 'vehicle_enquiry_temp':
            #pass  
            todo.local_backup(t,todo.in_e_id_sql,'enquiry_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data(t,todo.in_e_id_sql,'enquiry_id')
        elif t == 'insure_task_history':
            #pass  
            todo.local_backup(t,todo.in_e_id_sql,'enquiry_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data(t,todo.in_e_id_sql,'enquiry_id')
        elif t == 'order_item_info':
            #pass
            todo.local_backup('order_item_info',todo.in_e_id_sql,'quote_source_id')
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data('order_item_info',todo.in_e_id_sql,'quote_source_id')
        else:
            #pass
            todo.local_backup(t,todo.in_e_id_sql)
            todo.remote_backup(dest_database,t,todo.table_file)
            todo.delete_data(t,todo.in_e_id_sql)
    todo.delete_data('vehicle_enquiry',todo.in_e_id_sql,'id')
    todo.delete_data('ins_multi_quote',todo.in_m_id_sql,'id')
    todo.finish()
    content = ''
    for t in table_list:
        text = t+': local_backup={0},remote_backup={1},delete_data={2}'.format(local_backup_content[t],remote_backup_content[t],delete_data_content[t])
        content = content+text+'\n'
    todo.send_mail(mailto_list,mail_subject,content)
