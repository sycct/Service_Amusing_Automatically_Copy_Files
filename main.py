#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime

from utils import file_util


class AutomaticallyCopyFiles(object):
    def __init__(self):
        self._base_path = '/var/CDN/amusing'
        self._init_file = file_util.FileUtil()

    def copy_files_run(self):
        get_current_time = datetime.utcnow()
        file_list = self._init_file.get_file_list(self._base_path)
        print(file_list)


if __name__ == "__main__":
    AutomaticallyCopyFiles().copy_files_run()
