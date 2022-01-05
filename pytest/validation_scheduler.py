# -*- coding: utf-8 -*- 
"""
Created on 2021/9/22 15:23 
@File  : validation_scheduler.py
@author: zhoulu
@Desc  :
"""
from apscheduler.schedulers.blocking import BlockingScheduler
import pytest
import os
import time
import pandas as pd
from case.chandao_count import ChanDaoCount

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
    data.to_csv(file, index=False, encoding='utf-8')


def job_func():
    # , "stage环境" , "http://10.39.232.58"
    desc_list = ["生产环境"]
    env_list = ["pro"]
    url_list = ["http://10.39.232.56"]
    # 创建新线程
    for i in range(len(desc_list)):
        my_test = MyOneByOne(desc_list[i], env_list[i], url_list[i])
        my_test.run()
        time.sleep(2)


def chandao_job():
    ChanDaoCount().robot_send("http://project.itiaoling.com/zentao/user-login.html")


scheduler = BlockingScheduler()
# 在 2021-09-22 15:40:00 ~ 2022-09-22 15:40:00' 之间, 每天执行一次 job_func 方法 -days=1(每天触发）

# scheduler.add_job(job_func, 'interval', weeks=1, start_date='2021-12-08 09:00:00', end_date='2022-10-09 09:00:00')
scheduler.add_job(job_func, 'cron', day_of_week="tue", hour=9)
scheduler.add_job(chandao_job, 'cron', day_of_week="mon,tue,wed,thu,fri", hour=9, minute=1)

scheduler.start()
