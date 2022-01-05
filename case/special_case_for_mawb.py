# -*- coding: utf-8 -*- 
"""
Created on 2021/7/21 13:54 
@File  : special_case.py
@author: zhoul
@Desc  :
"""
import pandas
import os
from api.request_client import RequestClient
from commonfunc.handle_test_case import HandleTestCase
from commonfunc.get_faker import CreatData

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


def special_jt_case(origin_data, package_num):
    tracking_nums = []
    with open(rootPath + "\\data\\mawb\\mawb.txt", "r") as f:  # 打开文件
        tracking_nums = f.readlines()
        print(tracking_nums)
    for i in range(package_num):
        track = tracking_nums[i].replace("\n", "")
        print(track)
        data = str({
            "lastMileTrackingNumber": "%s"}
        ) % track
        tracking_nums.append(str(track))
        origin_data["data"]["packageInfoList"].append(eval(data))
    print(origin_data)
    return origin_data, tracking_nums


def get_test():
    ori_data = {
        "data": {
            "lastMileBagId": "20211122000001",
            "mawb": "003-20211122",
            "flightNumber": "MAWB(526-58571376)-FlightNumber(CN321)-ETD(2017-08-03T22:00:00+0800)-ETA(2017-08-04T10:00:00+0800)-DEPT(HKG)-ARR(LAX)-ATD(2017-08-03T22:00:00+0800)-ATA(2017-08-04T10:00:00+0800)",
            "grossWeight": 500,
            "packageInfoList": []
        },
        "messageId": "1620961843011",
        "timestamp": 1620961843011

    }
    handle = HandleTestCase()
    test_data, track = special_jt_case(ori_data, 200)
    req = RequestClient("http://10.39.232.53:8429")
    headers = {"Content-Type": "application/json"}

    result = req.get_request(path="/mawbInfo/v1/accept/jt", port="8429", method="post",
                             headers=headers,
                             params="", json_value=handle.get_deal_params("test", str(test_data)),
                             data="", file_value="")
    print(result)

    print(track)


get_test()
