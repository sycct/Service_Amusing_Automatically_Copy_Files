#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import paramiko


class FileUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def get_file_list(file_path):
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
            # os.path.getmtime() 函数是获取文件最后修改时间
            # os.path.getctime() 函数是获取文件最后创建时间
            dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(file_path, x)), reverse=True)
            # print(dir_list)
            return dir_list

    @staticmethod
    def copy_file(file_list, base_path):
        """
        两台服务器之间同步文件
        :param file_list: 文件名列表
        :param base_path: 远程文件路径
        :return:
        """
        remote_host = os.environ.get('TARGET_HOSTNAME')
        remote_user = os.environ.get('TARGET_USER')
        remote_password = os.environ.get('TARGET_PASSWORD')
        remote_port = int(os.environ.get('TARGET_PROT'))
        for item in file_list:
            print(item)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote_host, username=remote_user, password=remote_password, port=remote_port)
            sftp = ssh.open_sftp()
            # 本地文件路径
            local_file_path = os.path.join(base_path, item)
            # 由于远程文件与本地文件一样，所以目录也是一样的
            sftp.put(localpath=local_file_path, remotepath=local_file_path)
            sftp.close()
            ssh.close()
