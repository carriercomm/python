-- MySQL dump 10.13  Distrib 5.5.16, for Linux (x86_64)
--
-- Host: localhost    Database: yunwei
-- ------------------------------------------------------
-- Server version	5.5.16-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `cid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'city id',
  `city` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'city name ',
  `other` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (1,'广州',''),(2,'上海',''),(3,'北京','');
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config` (
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '运维服务器信息管理',
  `page` int(5) NOT NULL DEFAULT '10'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='系统配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;
INSERT INTO `config` VALUES ('运维服务器信息管理',30);
/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `history` (
  `hid` int(10) NOT NULL AUTO_INCREMENT,
  `content` text COLLATE utf8_unicode_ci NOT NULL COMMENT '还原SQL',
  `description` text COLLATE utf8_unicode_ci NOT NULL COMMENT '简介',
  `delman` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT '删除人',
  `deltime` int(11) NOT NULL COMMENT '删除时间',
  PRIMARY KEY (`hid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='历史记录表-删除操作';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hosts` (
  `hid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'host id',
  `hostname` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` int(3) NOT NULL,
  `project` int(3) DEFAULT NULL COMMENT 'some project',
  `idc` int(3) DEFAULT NULL COMMENT 'IDC infomation',
  `port` int(5) DEFAULT NULL,
  `addr1_ip` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr1_netmask` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr1_gateway` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr1_line` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr2_ip` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr2_netmask` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr2_gateway` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr2_line` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr3_ip` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr3_netmask` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr3_gateway` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addr3_line` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `memory` int(20) DEFAULT NULL,
  `cpu` int(20) DEFAULT NULL,
  `disk` int(20) DEFAULT NULL,
  `buytime` int(11) DEFAULT NULL COMMENT '购买时间',
  `servicetime` int(11) DEFAULT NULL COMMENT '质保时间',
  `hardwareinfo` text COLLATE utf8_unicode_ci,
  `bandwidth` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uses` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` int(20) DEFAULT '1',
  `company` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `os` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `other` text COLLATE utf8_unicode_ci,
  `jointime` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modifytime` int(20) NOT NULL DEFAULT '0',
  `modifyman` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hosts`
--

LOCK TABLES `hosts` WRITE;
/*!40000 ALTER TABLE `hosts` DISABLE KEYS */;
INSERT INTO `hosts` VALUES (1,'案例主机',1,1,1,22,'111.11.11.11','255.255.255.1','58.67.156.129','电信/公网','55.63.12.34','255.255.255.128','112.21.11.11','网通/内网','211.147.245.13','255.255.255.120','211.147.245.12','移动/其他',16,16,500,0,0,'---------------------------------\r\n案例条目\r\n---------------------------------\r\n机器品牌：\r\nCPU类型：\r\n硬盘类型：\r\nRAID类型：\r\n机柜编号：\r\n......\r\n......','100M共享','游戏服务器',1,'四海国际','CentOS6.2 64位','','1351651495',1352256730,'steven'),(2,'测试主机2',2,1,2,0,'','','','','','','','','','','','',0,0,0,0,0,'','','',3,'','','','1351653006',1351922375,'steven');
/*!40000 ALTER TABLE `hosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc`
--

DROP TABLE IF EXISTS `idc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc` (
  `iid` int(11) NOT NULL AUTO_INCREMENT,
  `city` int(6) NOT NULL COMMENT '所在城市',
  `idcname` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `contact` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hztime` int(11) DEFAULT NULL COMMENT '开始合作时间',
  `other` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`iid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc`
--

LOCK TABLES `idc` WRITE;
/*!40000 ALTER TABLE `idc` DISABLE KEYS */;
INSERT INTO `idc` VALUES (1,1,'测试IDC(广州)','',0,'测试IDC'),(2,2,'测试IDC(上海)','',0,'');
/*!40000 ALTER TABLE `idc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `other` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'测试项目','测试项目'),(2,'测试项目2','');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `sid` int(3) NOT NULL AUTO_INCREMENT,
  `status` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='主机状态表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'启用'),(2,'备用'),(3,'软件故障'),(4,'硬件故障'),(5,'停机');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'user ID',
  `privilege` int(3) NOT NULL COMMENT '0:visitor;1:Admin',
  `username` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `createtime` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'account create time',
  `lastlogin` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'last logined time',
  `loginip` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `other` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'other description',
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,2,'steven','f9e35bb10b58ca81bb841025bf7f4852','1351649903','1351922415','172.16.2.127','','','超级管理员\r\nhttp://johnsteven.blog.51cto.com/'),(2,0,'曹操','8607f43ab158e827826beaa1ca233025','1351652037','1351924391','172.16.2.127','','','测试账户');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-11-07 11:00:24
