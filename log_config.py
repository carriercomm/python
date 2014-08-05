#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
  
import logging  
import logging.config  
  
#日志初始化  
LOG_FILENAME = 'log.conf'  
logging.config.fileConfig(LOG_FILENAME)  
logger = logging.getLogger("simple_log_example")  
  
#测试代码  
logger.debug("debug message")  
logger.info("info message")  
logger.warn("warn message")  
logger.error("error message")  
logger.critical("critical message")
