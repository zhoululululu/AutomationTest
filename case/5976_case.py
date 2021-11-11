# -*- coding: utf-8 -*- 
"""
Created on 2021/7/19 9:35 
@File  : 5976_case.py
@author: zhoul
@Desc  :需求5976case，因为有大量的zipcode数据，所以批量测试
"""
import pandas
from api.request_client import RequestClient
import os
from commonfunc.db_client import MysqlClient
from commonfunc.datetime_tool import DateTimeTool

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class SINOSDKUpdateTest:
    def __init__(self):
        self.url = "http://10.39.232.133:8088"
        self.login_path = "/scorpio/users/v1/session"
        self.packages_path = "/scorpio/api/packages/v1/package"
        self.label_path = "/scorpio/api/packages/v1/printAgain/ES10000063740120001040001B0D"
        self.pre_label_path = "/scorpio/api/packages/v1/preAgainPrint/0/ES10000063740120001040001B0D"
        self.headers = {"Content-Type": "application/json"}
        self.request = RequestClient(self.url)
        self.login()
        self.sql = MysqlClient("dg_test")

    def login(self):
        login_data = {"userCode": "181471", "password": "650870b8f852071f45b99bb285f71a5c"}
        result = self.request.get_request(path=self.login_path, port="", method="post", headers=self.headers,
                                          json_value=login_data,
                                          file_value="")

    def get_packages(self):
        data = {
            "scanPackageTime": "2021-11-04 19:05:00",
            "packageWeight": "3000",
            "trackingNumber": "ES10000063740120001040001B0D",
            "endStatus": "null",
            "packageheight": 5,
            "packagewidth": 5,
            "packagelength": 40
        }

        packages_result = self.request.get_request(path=self.packages_path, port="", method="post",
                                                   headers=self.headers,
                                                   json_value=data,
                                                   file_value="")
        return packages_result

    def get_label(self):
        headers = {"token": self.request.session.cookies.get("rdc-token")}
        self.request.get_request(path=self.pre_label_path, port="", method="get",
                                 headers=headers,
                                 file_value="")
        label_result = str(self.request.get_request(path=self.label_path, port="", method="get", headers=headers,
                                                    file_value="")).replace("false", "'false'").replace("true",
                                                                                                        "'true'")
        label = eval(label_result)["result"][0]
        return label

    def change_zipcode(self, zipcode):
        str_list = ["0" for i in range(5 - len(str(zipcode)))]
        result_1 = ''.join(str_list) + str(zipcode)
        update = "UPDATE t_waybill_consignee SET consignee_zipcode = '%s' WHERE tracking_number = 'ES10000063740120001040001B0D'" % result_1
        result = self.sql.execute_sql(update)


if __name__ == '__main__':
    sino_test = SINOSDKUpdateTest()
    label_list = []
    data = pandas.read_excel(rootPath + "\\data\\Routing_file_economy_22092021 (1).xlsx")
    zipcode_list = data.CAP.tolist()
    routing_list = data.routingFile.tolist()
    for i in zipcode_list:

        sino_test.change_zipcode(i)
        sino_test.get_packages()
        label = sino_test.get_label()
        label_list.append(label)
        print(i, routing_list[zipcode_list.index(i)], label)
    result = pandas.DataFrame({"zipcode": zipcode_list, "routing_file": routing_list, "label": label_list})
    result.to_csv(rootPath + "\\testresults\\resultfile\\" + DateTimeTool.get_now_date() + "_6600_result.csv")
