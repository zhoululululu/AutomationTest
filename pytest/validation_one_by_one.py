# -*- coding: utf-8 -*- 
"""
Created on 2021/9/29 16:45 
@File  : thread_test.py
@author: zhoul
@Desc  :
"""

from commonfunc.get_logging import Logging
import threading
import time
import pandas as pd
import os
import pytest

logger = Logging()

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class MyOneByOne(object):

    def __init__(self, desc, env, url):
        self.desc = desc
        change_env(rootPath + "\\data\\" + "validation\\env.csv", desc, env, url)
        self.env, self.url = env, url

    def run(self):
        print("开启测试： %s" % self.desc)
        pytest.main(['-s', '-q', "test_validation.py"])
        print("退出测试： %s" % self.desc)


def change_env(file, desc, env, url):
    data = pd.read_csv(file, encoding='utf-8')
    data['desc'] = desc
    data['env'] = env
    data['url'] = url
    print("change_env", env, url)
    data.to_csv(file, index=False, encoding='utf-8')


desc_list = ["测试环境", "预发布环境", "stage环境", "生产环境"]
env_list = ["test", "pre", "stage", "pro"]
url_list = ["http://10.39.232.54", "http://10.39.232.52", "http://10.39.232.58", "http://10.39.232.56"]

# 创建新线程
for i in range(len(desc_list)):
    my_test = MyOneByOne(desc_list[i], env_list[i], url_list[i])
    my_test.run()
    time.sleep(2)
