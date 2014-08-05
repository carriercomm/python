1、获取帮助：
python Auto_deploy.py -h
2、上传key到keydir，重名为id_rsa并修改权限为600;
3、发布：
python Auto_deploy.py -d --base 'cipm' --part1 'go2 cm' --part3 'cm3'
4、回滚：
python Auto_deploy.py -r --base 'cipm' --part1 'go2 cm' --part3 'cm3'
