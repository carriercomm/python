#!/usr/bin/python
from optparse import OptionParser
import re, time, sys

usage = "Usage: %prog -i INTERFACE -t TIME [-w] [-c]"
parser = OptionParser(usage=usage)
parser.add_option("-i", "--interface",
                  type="string",
                  dest="interface",
                  default='eth0',
                  help="please specify a interface,default eth0,example eth0")
parser.add_option("-t", "--time",
                  type="int",
                  dest="time",
                  default=5,
                  help="please specify time interval (s),default 5,example 5")
parser.add_option("-l", "--loop",
                  type="int",
                  dest="loop",
                  default=0,
                  help="please specify loop value,value is 1 will loop print network flow,default 0")
parser.add_option("-w", "--warning",
                  type="int",
                  dest="warning",
                  default=6000,
                  help="please specify the warnig thresholds for transmit,receive unit is KB,default 6000,example 1000")
parser.add_option("-c", "--critical",
                  type="int",
                  dest="critical",
                  default=8000,
                  help="please specify the warnig thresholds for transmit,receive unit is KB,default 8000,example 1000")
(options, args) = parser.parse_args()
eth = options.interface
loop = options.loop
t = options.time
warning = options.warning
critical = options.critical


def get_eth_info():
    re_eth = eth + ':.*'
    eth_info = open('/proc/net/dev')
    info = eth_info.read()
    eth_info.close()
    r_eth = re.compile(re_eth)
    try:
        receive = r_eth.findall(info)[0].split(":")[1].split()[0]
    except:
        print "please specify a effective interface!"
        sys.exit(3)
    transmit = r_eth.findall(info)[0].split(":")[1].split()[8]
    return (transmit, receive)


def eth_flow():
    time1 = get_eth_info()
    time.sleep(t)
    time2 = get_eth_info()
    if int(time2[0]) < int(time1[0]):
        eth_transmit = int((4294967295 + int(time2[0]) - int(time1[0])) / 1024 / t)
    else:
        eth_transmit = int((float(time2[0]) - float(time1[0])) / 1024 / t)
    if int(time2[1]) < int(time1[1]):
        eth_receive = int((4294967295 + int(time2[1]) - int(time1[1])) / 1024 / t)
    else:
        eth_receive = int((float(time2[1]) - float(time1[1])) / 1024 / t)
    if eth_transmit > critical or eth_receive > critical:
        print "CRITICAL!!!%s in %d seconds network transmit and receive average(KB),transmit=%d,receive=%d |transmit=%dKB;%d;%d;receive=%dKB;%d;%d" % (
            eth, t, eth_transmit, eth_receive, eth_transmit, warning, critical, eth_receive, warning, critical)
        sys.exit(2)
    if eth_transmit > warning or eth_receive > warning:
        print "warning!!%s in %d seconds network transmit and receive average(KB),transmit=%d,receive=%d |transmit=%dKB;%d;%d;receive=%dKB;%d;%d" % (
            eth, t, eth_transmit, eth_receive, eth_transmit, warning, critical, eth_receive, warning, critical)
        sys.exit(1)
    if eth_transmit < warning and eth_receive < warning:
        print "OK!%s in %d seconds network transmit and receive average(KB),transmit=%d,receive=%d |transmit=%dKB;%d;%d;receive=%dKB;%d;%d" % (
            eth, t, eth_transmit, eth_receive, eth_transmit, warning, critical, eth_receive, warning, critical)
        sys.exit(0)
    else:
        print usage
        sys.exit(3)


def loop_eth_flow():
    time1 = get_eth_info()
    print "IN %d seconds network transmit and receive average(KB)" % t
    while True:
        time.sleep(t)
        time2 = get_eth_info()
        if int(time2[0]) < int(time1[0]):
            eth_transmit = int((4294967295 + int(time2[0]) - int(time1[0])) / 1024 / t)
        else:
            eth_transmit = int((float(time2[0]) - float(time1[0])) / 1024 / t)
        if int(time2[1]) < int(time1[1]):
            eth_receive = int((4294967295 + int(time2[1]) - int(time1[1])) / 1024 / t)
        else:
            eth_receive = int((float(time2[1]) - float(time1[1])) / 1024 / t)
        print "transmit=%s,receive=%s" % (eth_transmit, eth_receive)
        time1 = time2


if loop == 1:
    try:
        loop_eth_flow()
    except KeyboardInterrupt:
        print "User Press Ctrl+C,Exit"
    except EOFError:
        print "User Press Ctrl+D,Exit"
else:
    try:
        eth_flow()
    except KeyboardInterrupt:
        print "User Press Ctrl+C,Exit"
    except EOFError:
        print "User Press Ctrl+D,Exit"
