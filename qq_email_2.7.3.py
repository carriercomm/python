#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'liangsh'

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import smtplib
from email.mime.text import MIMEText
from email.Header import Header

mailto_list=['411947403@qq.com',]
mail_host="smtp.qq.com"
mail_port='465'
mail_user="476818061"
mail_pass="suker4134"
mail_postfix="qq.com"

def send_mail(to_list,sub,content):
    if isinstance(content,unicode):
        content = str(content)
    #me= ("%s<"+mail_user+">") % (Header('_mailFrom','utf-8'),)
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

if __name__ == '__main__':
    #if send_mail(mailto_list,"hello","hello world!你好"):
    if send_mail(mailto_list,"好","hello world!你好"):
        print "发送成功"
    else:
        print "发送失败" 
