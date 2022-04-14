# -*- coding: utf-8 -*-

import logging
import sys

from logging.handlers import TimedRotatingFileHandler

_FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(_FORMATTER)
    return console_handler


def get_file_handler(log_file='app.log'):
    file_handler = TimedRotatingFileHandler(
       filename=log_file,
       when='D',
       backupCount=5,
       encoding='UTF-8'
    )
    file_handler.setFormatter(_FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
