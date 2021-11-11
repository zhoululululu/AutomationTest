# -*- coding: utf-8 -*- 
"""
Created on 2021/9/8 16:18 
@File  : provide_api.py
@author: zhoul
@Desc  :
"""
import os
from flask import Flask, request, Response
from case.generate_tracking_number import GenerateTrackingNumber
from flask import jsonify
from case.rdc_flow import get_rdc_interface
from commonfunc.get_regular import GetRegular
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

app = Flask(__name__)  # 创建一个服务，赋值给APP


@app.route('/getTrackingNumber', methods=['POST'])
def download():
    env = request.json.get("env")  # 获取接口请求中form-data的url参数传入的值
    product = request.json.get("product")  # 获取接口请求中form-data的url参数传入的值
    num = request.json.get("num")  # 获取接口请求中form-data的url参数传入的值
    tracking_number = GenerateTrackingNumber().generate_tracking_num(env, product, num=int(num))
    data = {"tracking_number_list": tracking_number}
    return jsonify(data)


@app.route('/getSortingOrder', methods=['POST'])
def sorting_order():
    data = request.json.get("data")  # 获取接口请求中form-data的url参数传入的值
    result = {"result": get_rdc_interface("sorting_order", data)}
    return jsonify(result)


@app.route('/getRdcFlow', methods=['POST'])
def rdc_flow():
    data = request.json.get("data")  # 获取接口请求中form-data的url参数传入的值
    result = {"result": get_rdc_interface("rdc_order", data)}
    return jsonify(result)


@app.route('/getOrder', methods=['POST'])
def rdc_order():
    data = request.json.get("data")  # 获取接口请求中form-data的url参数传入的值
    result = {"result": get_rdc_interface("only_order", data)}
    return jsonify(result)


@app.route('/getRegular', methods=['POST'])
def get_regular():
    if "regx" not in str(request.form) or "test_data" not in str(request.form):
        result = {"error": "未获取regx/test_data参数, 请检查参数"}
        return Response(json.dumps(result), mimetype='application/json')
    else:
        regx = request.form.get("regx")
        test_data = eval(request.form.get("test_data"))
        try:
            data_length, result_count, error_data = GetRegular.get_regular_result(regx, test_data)
            result = {"正则测试总数量": data_length, "正则匹配数量": result_count, "正则未匹配数量": data_length - result_count,
                      "正则未匹配数据": error_data}
        except Exception as e:
            result = {"error": "正则匹配方法出错啦！"}
        return Response(json.dumps(result), mimetype='application/json')


app.run(host='0.0.0.0', port=8899, debug=True)
