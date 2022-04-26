#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from utils import file_util


class AutomaticallyCopyFiles(object):
    def __init__(self):
        # loading env config file
        dotenv_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        self._base_path = os.environ.get('BASE_PATH')
        self._init_file = file_util.FileUtil()

    def copy_files_run(self):
        # 计算一分钟以前的时间
        time_different = datetime.utcnow() - timedelta(minutes=1)
        # 按照时间到排序的文件列表
        file_list = self._init_file.get_file_list(self._base_path)
        # 需要复制的文件列表
        copy_file_list = []
        for file in file_list:
            # 获取当前文件
            file = os.path.getctime(os.path.join(self._base_path, file))
            # 当前文件创建时间，将时间戳转换成时间
            get_file_crate_time = datetime.fromtimestamp(file)
            if get_file_crate_time > time_different:
                # 如果是一分钟以内新建的文件加入文件列表
                copy_file_list.append(file)
        # 将需要复制的文件复制到远程服务器
        if copy_file_list:
            self._init_file.copy_file(copy_file_list, self._base_path)


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    copy_file = AutomaticallyCopyFiles()
    # 星期一早上 5：30：30 运行 automatically_update 自动更新
    scheduler.add_job(copy_file.copy_files_run, 'interval', minutes='1')
    # 开始运行调度器
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        exit(0)
