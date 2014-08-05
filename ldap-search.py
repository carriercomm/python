#!/usr/bin/env python
# -*- coding:utf8 -*-
# file: modify.py
import ldap
#import ldap.modlist

ld = ldap.initialize("ldap://10.68.3.67:389")
ld.simple_bind_s("cn=BaoWang_Admin,dc=baoxian,dc=com","secret")
print "root bind to LDAP SERVER success"
#print ld.search_s("o=dormforce.net, c=cn", ldap.SCOPE_SUBTREE, "ou=synx")
#print ld.search_s("o=organizations,dc=baoxian,dc=com", ldap.SCOPE_SUBTREE, "cn=920100463")
result_dict = ld.search_s("o=organizations,dc=baoxian,dc=com", ldap.SCOPE_SUBTREE, "cn=920100463")
#print ld.search_s("uid=04057445047247A1AE2F05D359C05411,ou=B8B0F0615CFB46BD964C92414F54641E,o=D5F273DE255D4CA38E2CFEDB6DDD0F52,o=68F5B804139440C5BC1AFC5B1D464264,o=96A9A2B0163F410EBF3B3D2ED22B5421,o=C203F2B43C67411E99E4E24A04FD410C,o=organizations,dc=baoxian,dc=com",ldap.SCOPE_SUBTREE)
#result_dict = ld.search_s("uid=04057445047247A1AE2F05D359C05411,ou=B8B0F0615CFB46BD964C92414F54641E,o=D5F273DE255D4CA38E2CFEDB6DDD0F52,o=68F5B804139440C5BC1AFC5B1D464264,o=96A9A2B0163F410EBF3B3D2ED22B5421,o=C203F2B43C67411E99E4E24A04FD410C,o=organizations,dc=baoxian,dc=com",ldap.SCOPE_SUBTREE)
print result_dict
#print result_dict[0][0]
#print result_dict[0][1].keys()
#for k in result_dict[0][1].keys():
#    print k+':'+unicode(result_dict[0][1][k][0], "utf-8")
#print result_dict[0][1]['displayName']
#print unicode(result_dict[0][1]['displayName'][0], "utf-8")
ld.unbind_s()
