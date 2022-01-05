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


def special_as_case(origin_data, package_num):
    tracking_nums = []
    # with open(rootPath + "\\data\\case.txt", "r") as f:  # 打开文件
    #     tracking_nums = f.readlines()
    for i in range(package_num):
        track = HandleTestCase().get_tracking_num()
        HandleTestCase().update_tracking_num(track)
        data = str({
            "trackingNumber": "%s",
            "referenceNumber": "%s",
            "consigneeFullName": "BOUCHRA",
            "consigneeBusinessName": "BOUCHRA",
            "consigneePhone": "1123123456",
            "consigneeCountry": "SG",
            "consigneeState": "state",
            "consigneeCity": "city",
            "consigneeDistrict": "Marl",
            "consigneeAddr1": "Allensteiner Str. 11",
            "consigneeAddr2": "",
            "consigneeAddr3": "",
            "consigneeZipCode": "145770",
            "sellerFullName": "Jackie Chan",
            "sellerBusinessName": "Jackie Chan",
            "sellerPhone": "12345678911",
            "sellerCountry": "CN",
            "sellerState": "BEIJING",
            "sellerCity": "BEIJING",
            "sellerDistrict": "DONGCHENG DISTRICT",
            "sellerAddr1": "fahuoren dizhiyi",
            "sellerAddr2": "",
            "sellerAddr3": "",
            "sellerZipCode": "123456",
            "lastMileServiceCode": "JTSGSTD",
            "packageHeight": 5.00,
            "packageLength": 40.00,
            "packageTotalValue": 6.91,
            "currency": "USD",
            "packageTotalWeight": 2000.00,
            "packageWidth": 5.00,
            "battery": 0,
            "incoterm": 0,
            "specialOperDesc1": "11",
            "itemInfoList": [
                {
                    "sku": "1611553510699",
                    "skuDesc": "CCEI-Test3",
                    "skuDescCn": "CCEI-测试3",
                    "skuValue": 6.91,
                    "currency": "USD",
                    "quantity": 1,
                    "skuWeight": 10.00,
                    "hscode": "010000",
                    "link": "www.ebay.com"
                }
            ]
        }) % (track, str(CreatData.get_num(10)))
        tracking_nums.append(str(track))
        origin_data["data"]["packageInfoList"].append(eval(data))
    print(origin_data)
    return origin_data, tracking_nums


def get_test():
    ori_data = {
        "data": {
            "project": "eBay",
            "businessCode": "LM&LH",
            "hoauBagId": "OCTEST20211123",
            "lastMileBagId": "OCTEST20211123",
            "bagWeight": 50,
            "vehicleNumber": "京12",
            "driverContactName": "12",
            "driverContactPhone": "12",
            "mawb": "526-58571376",
            "flightNumber": "MAWB(526-58571376)-FlightNumber(CA321)-ETD(2017-08-03T22:00:00+0800)-ETA(2017-08-04T10:00:00+0800)-DEPT(HKG)-ARR(LAX)-ATD(2017-08-03T22:00:00+0800)-ATA(2017-08-04T10:00:00+0800)",
            "lineHaulVendorName": "JT",
            "lastMileCountry": "MY",
            "lastMileGateWay": "PVG",
            "lastMileLocation": "ASD-TLV仓",
            "lastMileServiceCode": "JTSGSTD",
            "lastMileVendorName": "JT",
            "battery": 1,
            "incoterm": 0,
            "lengthUnit": 0,
            "weightUnit": 0,
            "packageInfoList": []
        }
    }
    handle = HandleTestCase()
    test_data, track = special_as_case(ori_data, 200)
    req = RequestClient("http://testx.orangeconnex.com")
    headers = {"Content-Type": "application/json"}

    result = req.get_request(path="/api/gemini-inner/jv-vendor/v1/confirmShipmentToJt", port="", method="post",
                             headers=headers,
                             params="", json_value=handle.get_deal_params("test", str(test_data)),
                             data="", file_value="")
    print(result)

    print(track)
get_test()
