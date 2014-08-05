#!/usr/bin/env python
# -*- coding:utf8 -*-
# file: modify.py
import ldap
import ldap.modlist

ld = ldap.initialize("ldap://10.68.3.67:389")
ld.simple_bind_s("cn=BaoWang_Admin,dc=baoxian,dc=com","secret")
print "root bind to LDAP SERVER success"
result_dict = ld.search_s("o=organizations,dc=baoxian,dc=com", ldap.SCOPE_SUBTREE, "cn=920100463")
dn = result_dict[0][0]
print dn
#newuid = [('uid=11111111111111111,ou=F5D3BAD692354D9F8315E11A1C932869,o=9F327107B05E449388BA0799AC2DFCDE,o=D38FCB1AA107438D9A871AA25B4FA503,o=F68C4EE79C4146AB8F4267111E7DF386,o=C203F2B43C67411E99E4E24A04FD410C,o=organizations,dc=baoxian,dc=com', {'description': ['2013-12-27 14:50:24.828'], 'registeredAddress': ['450305761113103'], 'displayName': ['\xe7\x94\x98\xe6\x99\x93\xe6\x98\x8e'], 'cn': ['920100463'], 'businessCategory': ['01'], 'title': ['PropertyIns'], 'objectClass': ['inetOrgPerson'], 'userPassword': ['{MD5}SlWKTWmsdpyKMG/1qgGJTw=='], 'labeledURI': ['serialNumber=863371010181494,o=895CB09CA933484C82ECDB2339C6DCCB,o=C203F2B43C67411E99E4E24A04FD410C,o=organizations,dc=baoxian,dc=com'], 'initials': ['1'], 'mobile': ['11111111113'], 'employeeNumber': ['920100463'], 'sn': ['\xe7\x94\x98'], 'givenName': ['\xe6\x99\x93\xe6\x98\x8e'], 'uid': ['2957DB67EC61450E9EA45F75DFCA725F']})]
#oldAttrDict = {'mobile':['13822268369'],'registeredAddress':['430111199111111324'],'displayName':['蒋桂婷']}
oldAttrDict = {'mobile':['11111111112'],}
#oldAttrDict = {'mobile':['11111111112'],'uid':['2957DB67EC61450E9EA45F75DFCA725F']}
#newAttrDict = {'mobile':['18665674621'],'registeredAddress':['430424198410125412'],'displayName':['邱正']}
newAttrDict = {'mobile':['11111111113'],}
#newAttrDict = {'mobile':['11111111112'],'uid':['11111111111111111111111111111111']}
#ldap.modlist.modifyModlist(olduid,newuid)
#modList = ldap.modlist.modifyModlist(oldAttrDict,newAttrDict)
#ld.modify_s("uid=2957DB67EC61450E9EA45F75DFCA725F,ou=F5D3BAD692354D9F8315E11A1C932869,o=9F327107B05E449388BA0799AC2DFCDE,o=D38FCB1AA107438D9A871AA25B4FA503,o=F68C4EE79C4146AB8F4267111E7DF386,o=C203F2B43C67411E99E4E24A04FD410C,o=organizations,dc=baoxian,dc=com", modList)
#ld.modify_s(uid, modList)
ld.modrdn_s(dn,'uid=fuck', True)
#ld.modrdn_s(olduid,'uid=dddddd', False)
ld.unbind_s()
