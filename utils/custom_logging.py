# /usr/bin python3
# -*- encoding:utf-8 -*-
# create date: 2023/8/27
# create time: 13:21
# create author: 93207
# desc: 基于系统 logging 的log方法

import os
import logging
import datetime
import logging.handlers


class Logger:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_name = kwargs.get("log_name") or __name__
        self.log_path = kwargs.get("log_path") or "logs"
        self.when = kwargs.get("when") or "D"
        self.interval = kwargs.get("interval") or 1
        self.backupCount = kwargs.get("backupCount") or 7
        self.encoding = kwargs.get("encoding") or "utf-8"

        default_format = (
            "[%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s]: %(message)s"
        )
        fmt = kwargs.get("format") or default_format
        self.fmt = logging.Formatter(fmt)

        current_day_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.date_log_path = f"{self.log_path}{os.sep}{current_day_time}"
        if not os.path.exists(self.date_log_path):
            os.makedirs(self.date_log_path, exist_ok=True)

        self.log = logging.getLogger(self.log_name)
        self.log.setLevel(logging.DEBUG)

        if not self.log.handlers:
            self.__stream_log_handler()
            self.__info_file_log_handler()
            self.__error_file_log_handler()

    def __stream_log_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.fmt)
        console_handler.setLevel(logging.INFO)
        self.log.addHandler(console_handler)

    def __info_file_log_handler(self):
        info_file_name = f"{self.date_log_path}{os.sep}{self.log_name}_info.log"
        info_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=info_file_name,
            when=self.when,
            interval=self.interval,
            backupCount=self.backupCount,
            encoding=self.encoding,
        )
        info_file_handler.setLevel(logging.DEBUG)
        info_file_handler.setFormatter(self.fmt)
        info_file_handler.suffix = "%Y-%m-%d.log"
        info_file_handler.addFilter(lambda record: record.levelno <= 30)
        self.log.addHandler(info_file_handler)

    def __error_file_log_handler(self):
        error_file_name = f"{self.date_log_path}{os.sep}{self.log_name}_error.log"
        error_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=error_file_name,
            when=self.when,
            interval=self.interval,
            backupCount=self.backupCount,
            encoding=self.encoding,
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(self.fmt)
        error_file_handler.suffix = "%Y-%m-%d.log"
        self.log.addHandler(error_file_handler)
