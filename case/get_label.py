# -*- coding: utf-8 -*- 
"""
Created on 2021/11/10 17:22 
@File  : get_label.py
@author: zhoul
@Desc  :
"""

from config.get_config import Config
from api.request_client import RequestClient


class GetLabel(object):

    def __init__(self, env, rdc, tracking_umber):
        self.urls = Config("url").get_urls(env, rdc)
        self.tracking_number = tracking_umber
        self.headers = {"Content-Type": "application/json"}
        self.request = RequestClient("")
        self.login()

    def login(self):
        login_data = {"userCode": self.urls["username"], "password": self.urls["password"]}
        self.request.get_request(path=self.urls["login_path"], port="", method="post", headers=self.headers,
                                 json_value=login_data,
                                 file_value="")

    def get_label(self):
        self.login()
        headers = {"token": self.request.session.cookies.get("rdc-token")}
        before_result = self.request.get_request(path=self.urls["pre_label"] + self.tracking_number, port="",
                                                 method="get",
                                                 headers=headers,
                                                 file_value="")
        print(before_result)
        act_service_code = before_result["result"].get("vendorServiceCode")
        label_result = str(
            self.request.get_request(path=self.urls["again_label"] + self.tracking_number, port="", method="get",
                                     headers=headers,
                                     file_value="")).replace("false", "'false'").replace("true",
                                                                                         "'true'")
        label = eval(label_result)["result"][0]
        print(act_service_code, label)
        return act_service_code, label


if __name__ == '__main__':
    GetLabel("test", "dg", "ES10000063761730001040001D0D").get_label()
