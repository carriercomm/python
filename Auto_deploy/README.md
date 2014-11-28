1、获取帮助：
python Auto_deploy.py -h
2、上传key到keydir，重名为自己的名称，如liangshuhua，并修改权限为600;
3、发布：
python Auto_deploy.py -d --base 'cipm' --part 'go2 cm'
4、回滚：
python Auto_deploy.py -r --base 'cipm' --part 'go2 cm'

-------
1、脚本目录结构介绍
.
├── Auto_deploy.py         （发布脚本入口，调各个子脚本完成自动发布任务）
├── Colorer.py             （标准输出的颜色控制，info级别的输出为绿色，error级别的输出为红色）
├── config.py              （发布脚本的配置文件，定义应用的IP地址，应用类型等）
├── configuredir           （各个应用的配置文件目录，如go2，cm...）
│   ├── go2                （一区go2的配置目录）
│   ├── cipm               （一区供应商的配置目录）
│   ├── cm                 （一区cm的配置目录）
│   ├── cx                 （一区车型库的配置目录）
│   ├── dataTransform      （一区核心同步的配置目录）
│   ├── engine             （一区规则引擎的配置目录）
│   ├── order              （一区定单的配置目录）
│   ├── radar              （一区投保流程2.0的配置目录）
│   ├── rb                 （一区rb的配置目录）
│   ├── renewal            （一区快速续保的配置目录）
│   ├── task-dispatcher    （一区新调度的配置目录）
├── core.py                （主脚本，主要功能有文件传输，远程登陆，配置文件生成等）
├── deploydir              （此目录不需要关注，由脚本自动生成。发布脚本自动将应用的配置及数据分别发到conf跟html目录下）
│   ├── go2
│   │   ├── conf
│   │   └── html
│   ├── cipm
│   │   ├── conf
│   │   └── html
│   ├── cm
│   │   ├── conf
│   │   └── html
│   ├── cx
│   │   ├── conf
│   │   └── html
│   ├── dataTransform
│   │   ├── conf
│   │   └── html
│   ├── engine
│   │   ├── conf
│   │   └── html
│   ├── order
│   │   ├── conf
│   │   └── html
│   ├── radar
│   │   ├── conf
│   │   └── html
│   ├── rb
│   │   ├── conf
│   │   └── html
│   ├── renewal
│   │   ├── conf
│   │   └── html
│   ├── task-dispatcher
│       ├── conf
│       └── html
├── keydir                （远程登陆服务器key的存放目录）
│   ├── hongyuhuai
│   └── liangshuhua
├── log.conf              （发布脚本日志的配置文件）
├── README.md             （发面脚本介绍文件）
├── rollbackdir           （发布回滚的目录，由脚本自动生成）
│   ├── go2
│   │   └── undo
│   ├── cipm
│   │   └── undo
│   ├── cm
│   │   └── undo
│   ├── cx
│   │   └── undo
│   ├── dataTransform
│   │   └── undo
│   ├── engine
│   │   └── undo
│   ├── order
│   │   └── undo
│   ├── radar
│   │   └── undo
│   ├── rb
│   │   └── undo
│   ├── renewal
│   │   └── undo
│   ├── task-dispatcher
│   │   └── undo
├── softdir              （需要发布的包存放目录，需要将包解压到相应的目录下）
│   ├── cipm             （供应商的发布包存放目录，需要将war包解压放到此目录下）
│   ├── cm
│   ├── cx
│   ├── dataTransform
│   ├── engine
│   ├── go2
│   ├── order
│   ├── radar
│   ├── rb
│   ├── renewal
│   └── task-dispatcher
├── tasks.py             （发布脚本的逻辑控制部分，如控制发布应用的类型，分区等）

2、脚本参数说明：
-h/--help(打印帮助信息)、-d(执行发布)、-r(执行回滚)、--base(基础应用)、--part(分区应用)

3、脚本使用例子
使用的话只需要关注三个目录，分别为keydir，softdir，configuredir。
3.1 完整包发布的步骤如下：
3.1.1将自己的key文件传到keydir目录下，重命名（如贺艳芳的key就改成heyanfang）及修改权限(chmod 600 heyanfang);
3.2.2将要发布的包解压到softdir对应的目录下（如发布go2，就将go2的war包解压到softdir/go2目录下）;
3.2.3修改应用的配置文件（如二区go2需要修改xmpp.properties配置文件，去到configuredir/carbiz2下，修改xmpp.properties后保存），如果配置文件没有变化此步跳过。
完成上面三步后就可以开始执行发布脚本，完成自动发布，
如全区发布go2:
./Auto_deploy.py -d --part 'go2 carbiz2 carbiz3 carbiz4 carbiz5 carbiz6'
3.2 class或jar包发布步骤如下：
如发布go2的一些class，去到目录softdir/go2/WEB-INF/...，替换新的class，执行发布脚本
./Auto_deploy.py -d --part 'go2 carbiz2 carbiz3 carbiz4 carbiz5 carbiz6'
3.3 发布回滚
如需要回滚刚才发布的go2，执行./Auto_deploy.py -r --part 'go2 carbiz2 carbiz3 carbiz4 carbiz5 carbiz6'
回滚是回滚到最后一次发布的状态。

