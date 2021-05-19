# -*- coding: utf-8 -*-
# @File  : request_client.py
# @Author: 周璐
# @Date  : 2021/5/19 22:25
# @Desc  :
import requests


class RequestClient:

    def __init__(self):
        pass

    @classmethod
    def update_header(cls, file):
        pass

    @classmethod
    def get_request(cls, url, method, headers, data=None, params=None, file=None):
        result = requests.request(url=url, method=method,
                                  headers=headers if file is None else RequestClient.update_header(file),
                                  params=params if params is not None else None,
                                  data=data if data is not None else None,
                                  file=file if file is not None else None )


class ResponseClient:

    def __init__(self):
