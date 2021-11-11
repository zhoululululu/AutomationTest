# -*- coding: utf-8 -*- 
"""
Created on 2021/9/28 18:05 
@File  : pytest_1.py
@author: zhoul
@Desc  :
"""

import pytest


def test_03():
    print('测试用例3操作')


def test_04():
    print('测试用例4操作')


def test_05():
    print('测试用例4操作')


def test_06():
    print('测试用例4操作')


def test_07():
    print('测试用例4操作')


def test_08():
    print('测试用例4操作')


if __name__ == "__main__":
    pytest.main(["-s", "test_1.py", '--workers=2', '--tests-per-worker=4'])
