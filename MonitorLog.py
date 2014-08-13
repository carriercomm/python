#!/usr/bin/env python
# encoding: utf-8
  
"""
MonitorLog.py
  
Usage: MonitorLog.py ...
Monitor the log file
  
-f  log file
-h  help info
  
python MonitorLog.py -f C:\monitor.log
  
Created by Liangsh on 2014-08-13.
"""

import sys
import os
import getopt
import subprocess
import time
import codecs
#import winsound
import smtplib
from email.mime.text import MIMEText
from email.Header import Header

####
#mailto_list=['hongyh@baoxian.com','liangsh@baoxian.com']
mailto_list=['liangsh@baoxian.com',]
mail_host="smtp.qq.com"
mail_port='465'
mail_user="2081276696"
mail_pass="cninsure2013"
mail_postfix="qq.com"
mail_subject='一区TC监控-'+str(datetime.date.today().strftime('%Y%m%d'))

ABSPATH = os.path.dirname(os.path.abspath(__file__))
MONITERCONF = 'moniter_keyword.txt' #utf8 file

def send_mail(to_list,sub,content):
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


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:')
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        return 1
  
    path = ''
    for k, v in opts:
        if k == '-f':
            path = v
        elif k == '-h':
            print __doc__
            return 0
  
    if not (path and os.path.exists(path)):
        print 'Invalid path: %s' % path 
        print __doc__
        return 2
  
    #命令行元组
    cmd = ('tail', '-f', path)
    print ' '.join(cmd)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  
    keywordMap = {}
    #加载监控的关键字信息
    with codecs.open(os.path.join(ABSPATH, MONITERCONF), 'r', 'utf8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        keyword, wav = line.strip().split(':')
        keywordMap[keyword] = wav
  
    while True:
        line = output.stdout.readline()
        #process code,得到输出信息后的处理代码
        if not line:
            time.sleep(0.01)
            continue
        line = line.strip().decode('utf8')
        #print line
        for keyword in keywordMap:
            if line.find(keyword) > -1:
                #winsound.PlaySound(keywordMap[keyword], winsound.SND_NODEFAULT)
				send_mail(mailto_list,mail_subject,"一区tc故障")
        #time.sleep(0.01)
    return 0
  
if __name__ == '__main__':
    sys.exit(main()) 
