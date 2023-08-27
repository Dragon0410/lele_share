# /usr/bin python3
# -*- encoding:utf-8 -*-
# create date: 2023/8/27
# create time: 13:21
# create author: 93207
# desc:


import datetime
import os
import sys

from loguru import logger


class Logger:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_name = kwargs.get("log_name") or __name__
        self.log_path = kwargs.get("log_path") or "logs"
        self.retention = kwargs.get("retention") or "7days"
        self.rotation = kwargs.get("rotation") or "500MB"
        self.encoding = kwargs.get("encodings") or "utf-8"

        default_format = "[{time} | {file}({line}) | {level}]: {message}"
        self.fmt = kwargs.get("format") or default_format

        current_day_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.date_log_path = f"{self.log_path}{os.sep}{current_day_time}"
        if not os.path.exists(self.date_log_path):
            os.makedirs(self.date_log_path, exist_ok=True)

        self.log = logger
        self.log.remove()

        # 终端
        self.log.add(sys.stdout, level="INFO", colorize=True)

        # 文件
        info_file_handler = f"{self.date_log_path}{os.sep}{self.log_name}_info.log"
        self.log.add(
            info_file_handler,
            level="DEBUG",
            filter=lambda x: x["level"].no <= 20,
            format=self.fmt,
            retention=self.retention,
            rotation=self.rotation,
            encoding=self.encoding,
        )

        error_file_handler = f"{self.date_log_path}{os.sep}{self.log_name}_error.log"
        self.log.add(
            error_file_handler,
            level="ERROR",
            filter=lambda x: x["level"].no > 20,
            format=self.fmt,
            retention=self.retention,
            rotation=self.rotation,
            encoding=self.encoding,
        )


