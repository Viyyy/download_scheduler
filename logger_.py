# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-04-01 14:43:52
# Description: This is a logger configuration file.

''' 
# Usage example
from common.logger import logging

logger = logging.getLogger(__name__)

logger.info("Hello, world!")
logger.debug("This is a debug message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
'''

import logging
import logging.config
import colorlog
    
LOG_FILE = "app.log" # 写入的日志文件的名称
ERROR_LOG_FILE = "error.log" # 写入的错误文件的名称
    
# 创建一个 ColorFormatter
color_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

class LogConfig:
    def __init__(self, log_file, error_log_file):
        self.log_file = log_file
        self.error_log_file = error_log_file
        self.load_config()
        
    def __get_config__(self):
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "color_formatter": {
                    "()": colorlog.ColoredFormatter,
                    "format": "%(log_color)s[%(asctime)s]-%(levelname)s from %(name)s:%(message)s",
                    "log_colors": {
                        "DEBUG": "cyan",
                        "INFO": "green",
                        "WARNING": "yellow",
                        "ERROR": "red",
                        "CRITICAL": "red,bg_white",
                    },
                },
                'text_formatter':{
                    "format":"[%(asctime)s]-%(levelname)s from %(name)s:%(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "color_formatter",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "text_formatter",
                    "filename": self.log_file,  # 你想要写入的日志文件的名称
                    "mode": "a",  # 附加模式，如果你想要覆盖文件，可以使用 'w'
                },
                "error_file": {
                    "class": "logging.FileHandler",
                    "level": "ERROR",
                    "formatter": "text_formatter",
                    "filename": self.error_log_file,  # 你想要写入的错误文件的名称
                    "mode": "a",  # 附加模式，如果你想要覆盖文件，可以使用 'w'
                },
            },
            "root": {"level": "DEBUG", "handlers": ["console", "file", "error_file"]},
        }
        return log_config
    
    def load_config(self):
        log_config = self.__get_config__()
        logging.config.dictConfig(log_config)

LOG_CONFIG = LogConfig(LOG_FILE, ERROR_LOG_FILE)