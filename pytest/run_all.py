# -*- coding: UTF-8 -*-
# coding=utf-8
'''
Created on 2021/7/5
@File  : run_all.py
@author: ZL
@Desc  :
'''
import pytest
import os
import sys
import subprocess

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

if __name__ == '__main__':
    """
    pytest批量运行测试case ，-m可单独运行特定的case
    生成结果文件，并生成压缩文件，发送email
    """
    # pytest.main(['-s', '-q', '--alluredir', rootPath + '/testresults/pytestresult/data', "-m=validation"])
    # subprocess.run(['allure', 'generate', rootPath + '/testresults/pytestresult/data', '-o',
    #                 rootPath + '/testresults/pytestresult/data/html', '--clean'], shell=True)

    # env_name = os.environ["TEST"]
    # env_no = os.environ["http://10.39.232.54"]
    # pytest_args = ("TEST", "http://10.39.232.54")
    os.system("pytest  --base--url http://10.39.232.54")


    # # 调用zip_file方法，生成压缩文件
    # zipfile = CommonFunction.zip_file(rootPath + '\\testresults\\pytestresult\\data\\html',
    #                                   rootPath + '\\testresults\\result.zip')
    # send_email = SendEmail()
    # send_email.send_email(rootPath + '\\testresults\\result.zip')  # 发送email附上附件
