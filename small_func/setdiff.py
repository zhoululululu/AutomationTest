# -*- coding: utf-8 -*-
# @Time    : 2021/4/30 16:21
# @Author  : Zhou
# @File    : setdiff.py
# @Software: PyCharm
import json
import pandas
import random
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


def setdiff():
    post_code_pre = sorted(
        set(["010", "011", "012", "013", "014"]))
    post_code = []
    for i in range(0, 1000):
        if i < 10:
            post_code.append('00' + str(i))
        elif i < 100:
            post_code.append('0' + str(i))
        else:
            post_code.append('' + str(i))
    print(sorted(list(set(post_code) - set(post_code_pre))))


def get_diff2(list1, list2):
    print(sorted(list(set(list1) - set(list2))))


def get_test1():
    print('{:.2%}'.format(31 / 33))
    print(str(random.randint(0000, 9999)))


# get_test1()


def get_tracking():
    result_tracking_list = []
    file_1 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028103729_SP_101_01_error.csv")
    file_2 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028103936_SP_101_01_error.csv")
    file_3 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028103948_SP_101_01_error.csv")
    file_4 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028115031_SP_101_01_error.csv")
    file_5 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028115457_SP_101_01_error.csv")

    result_tracking_list += file_1["trackingNumber"].tolist()
    result_tracking_list += file_2["trackingNumber"].tolist()
    result_tracking_list += file_3["trackingNumber"].tolist()
    result_tracking_list += file_4["trackingNumber"].tolist()
    result_tracking_list += file_5["trackingNumber"].tolist()
    print(list(set(result_tracking_list)))
    print(len(list(set(result_tracking_list))))


# get_tracking()

def small():
    print(len(str(12)))
    str_lsit = ["0" for i in range(5 - len(str(12)))]
    print(str_lsit)
    print(type(str_lsit))
    result = ''.join(str_lsit)
    print(result+str(12))
small()
