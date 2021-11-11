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


class MyThread(threading.Thread):

    def __init__(self, thread_id, thread_name, env, url):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        change_env(thread_id, rootPath + "\\data\\" + "validation\\env.csv", env, url)
        self.env, self.url = env, url

    def run(self):
        print("开启线程： %s" % self.thread_id)
        pytest.main(['-s', '-q', "test_validation.py"])
        queueLock.acquire()
        time.sleep(1)
        print("退出线程： %s" % self.thread_name)
        queueLock.release()


def change_env(thread_id, file, env, url):
    data = pd.read_csv(file, encoding='utf-8')
    data['env'] = env
    data['url'] = url
    print("change_env", thread_id, env, url)
    data.to_csv(file, index=False, encoding='utf-8')


thread_list = ["Thread-测试环境", "Thread-预发布环境", "Thread-stage环境", "Thread-生产环境"]
env_list = ["test", "pre", "stage", "pro"]
url_list = ["http://10.39.232.54", "http://10.39.232.52", "http://10.39.232.58", "http://10.39.232.56"]
queueLock = threading.Lock()
threads = []
threadID = 1

# 创建新线程
for i in range(len(thread_list)):
    thread = MyThread(threadID, thread_list[i], env_list[i], url_list[i])
    thread.start()
    threads.append(thread)
    threadID += 1
    time.sleep(3)

# 等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")
