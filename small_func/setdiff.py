# -*- coding: utf-8 -*-
# @Time    : 2021/4/30 16:21
# @Author  : Zhou
# @File    : setdiff.py
# @Software: PyCharm
import json
import pandas
import random
from commonfunc.file_manage import FileManage
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


def replace_some(file):
    test_data = FileManage.file_to_dict(file, sheet_name="Sheet1")
    test_list = test_data.get("test").tolist()
    for i in test_list:
        data = eval(i)
        data["dropSiteInfo"] = '{"siteId":"YW06","siteName":"YW杭州站","contactName":"周衍","contactTel":"13588325176","dropSiteCountry":"CN","dropSiteState":"330000","dropSiteCity":"330100","dropSiteDistrict":"330108","dropSiteAddr1":"杭州市萧山区保税物流园8号仓","dropSiteAddr2":"","dropSiteAddr3":""}'
        print(data)

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
    # result_tracking_list = []
    file_1 = pandas.read_excel(rootPath + "\\data\\jitu\\jt-order.xlsx", sheet_name='SGtrackingNumber')
    # file_2 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028103936_SP_101_01_error.csv")
    # file_3 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028103948_SP_101_01_error.csv")
    # file_4 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028115031_SP_101_01_error.csv")
    # file_5 = pandas.read_csv(rootPath + "\\data\\test_file\\" + "20211028115457_SP_101_01_error.csv")
    final = []
    result = file_1["跟踪号码"].tolist()
    print(sorted(result, reverse=False))
    # if len(str(i)) ==5:
    #     final.append("0"+str(i))
    # else :

    # with open("test.txt", "w") as f:
    #     for i in result:
    #         if len(str(i)) == 5:
    #             f.write('"0' + str(i) + '",')
    #         else :
    #         # final.append((str(i).replace("'", '"')))
    #             f.write('"' + str(i) + '",')
    # result_tracking_list += file_2["trackingNumber"].tolist()
    # result_tracking_list += file_3["trackingNumber"].tolist()
    # result_tracking_list += file_4["trackingNumber"].tolist()
    # result_tracking_list += file_5["trackingNumber"].tolist()
    # print(list(set(result_tracking_list)))
    # print(len(list(set(result_tracking_list))))
    # print(result)
    # print(final)


# get_tracking()

def small():
    print(len(str(12)))
    str_lsit = ["0" for i in range(5 - len(str(12)))]
    print(str_lsit)
    print(type(str_lsit))
    result = ''.join(str_lsit)
    print(result + str(12))


def str_str():
    str = "string"
    print(str[3:4])


replace_some(rootPath + "\\data\\" + "validation\\validation-case.xlsx")
