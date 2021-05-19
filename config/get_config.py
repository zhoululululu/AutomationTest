# -*- coding: UTF-8 -*-
'''
Created on 2020/2/29
@File  : get_config.py
@author: ZL
@Desc  :
'''

import os

from commonfunc.common_tool import PublicTool

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Config(object):
    def __init__(self):
        """
        初始化config，读取config文件
        """
        self.config = PublicTool()
        self.file_path = rootPath + "\\config\\config.yaml"
        # self.config.read_yaml(rootPath + "\\testdata\\config.txt", encoding='UTF-8')
        self.conf = {}

    def get_email_info(self):
        """
        获取email的各种参数配置值
        """
        self.conf['service'] = self.config.read_yaml(self.file_path, "Email", "service")
        self.conf['version'] = self.config.read_yaml(self.file_path, "Email", "version")
        self.conf['tester'] = self.config.read_yaml(self.file_path, "Email", "tester")
        self.conf['remark'] = self.config.read_yaml(self.file_path, "Email", "remark")
        self.conf['is_send'] = self.config.read_yaml(self.file_path, "Email", "is_send")
        self.conf['user'] = self.config.read_yaml(self.file_path, "Email", "user")
        self.conf['password'] = self.config.read_yaml(self.file_path, "Email", "password")
        self.conf['host'] = self.config.read_yaml(self.file_path, "Email", "host")
        self.conf['rec_users'] = self.config.read_yaml(self.file_path, "Email", "rec_users")
        self.conf['title'] = self.config.read_yaml(self.file_path, "Email", "title")
        return self.conf

    def get_sql_info(self):
        """
        获取mql数据库的各种参数配置值
        """
        self.conf['mql_host'] = self.config.read_yaml(self.file_path, "Mysql", "db_host")
        self.conf['mql_port'] = self.config.read_yaml(self.file_path, "Mysql", "db_port")
        self.conf['mql_user_name'] = self.config.read_yaml(self.file_path, "Mysql", "user_name")
        self.conf['mql_user_pwd'] = self.config.read_yaml(self.file_path, "Mysql", "user_pwd")

        return self.conf

    def get_oracle_info(self):
        """
        获取oracle数据库的各种参数配置值
        """
        self.conf['oracle_host'] = self.config.read_yaml(self.file_path, "Oracle", "oracle_host")
        self.conf['oracle_port'] = self.config.read_yaml(self.file_path, "Oracle", "oracle_port")
        self.conf['oracle_user_name'] = self.config.read_yaml(self.file_path, "Oracle", "oracle_user_name")
        self.conf['oracle_user_pwd'] = self.config.read_yaml(self.file_path, "Oracle", "oracle_user_pwd")

        return self.conf

    def get_es_info(self):
        """
        获取ES的各种参数配置值
        """
        self.conf['es_host'] = self.config.read_yaml(self.file_path, "ES", "ip")
        self.conf['es_port'] = self.config.read_yaml(self.file_path, "ES", "port")
        self.conf['es_user_name'] = self.config.read_yaml(self.file_path, "ES", "user_name")
        self.conf['es_user_pwd'] = self.config.read_yaml(self.file_path, "ES", "user_pwd")

        return self.conf

    def get_redis_info(self, env):
        """
        获取redis的各种参数配置值
        """
        self.conf['redis_ip'] = self.config.read_yaml(self.file_path, env, "redis_ip")
        self.conf['redis_port'] = self.config.read_yaml(self.file_path, env, "redis_port")
        return self.conf

    def get_ssh_info(self):
        """
        获取堡垒机的各种参数配置值
        """
        self.conf['ssh_ip'] = self.config.read_yaml(self.file_path, "SSH", "ssh_ip")
        self.conf['ssh_port'] = self.config.read_yaml(self.file_path, "SSH", "ssh_port")
        self.conf['ssh_name'] = self.config.read_yaml(self.file_path, "SSH", "ssh_name")
        self.conf['ssh_pwd'] = self.config.read_yaml(self.file_path, "SSH", "ssh_pwd")

        return self.conf


if __name__ == '__main__':
    demo = Config()
    print(demo.get_email_info())
