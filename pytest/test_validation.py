# -*- coding: utf-8 -*- 
"""
Created on 2021/7/2 11:26 
@File  : test_validation.py
@author: zhoul
@Desc  :
"""
import os
from commonfunc.file_manage import FileManage
from commonfunc.datetime_tool import DateTimeTool
import pytest
import allure
from api.request_client import RequestClient
from commonfunc.assert_tool import AssertTool
from commonfunc.handle_test_case import HandleTestCase
import pandas
from commonfunc.beauty_excel import beauty_format
from commonfunc.wx_robot import WeChat

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class TestValidation(object):
    global file_name, all_data, test_case
    file_name = rootPath + "\\data\\" + "validation\\validation-case.xlsx"
    all_data = FileManage.file_to_dict(file_name)
    test_case = all_data.get("case_manage").fillna("").values

    def setup_class(self):
        """
        :return:
        """
        self.handle = HandleTestCase()
        env_data = FileManage.file_to_dict(rootPath + "\\data\\" + "validation\\env.csv")
        self.env_desc, self.env, self.url = env_data.get("desc")[0], env_data.get("env")[0], env_data.get("url")[0]
        self.req = RequestClient(self.url)
        self.error_des_list, self.error_data_list, self.error_res_list, self.error_assert_list, self.error_exp_list, self.error_act_list, self.error_service_list, self.error_file_list = [], [], [], [], [], [], [], []
        self.all_des_list, self.all_data_list, self.all_res_list, self.all_assert_list, self.all_exp_list, self.all_act_list, self.all_service_list, self.all_file_list = [], [], [], [], [], [], [], []
        self.all_num, self.error_num, self.success_num, self.skip_num = 0, 0, 0, 0

    @pytest.mark.parametrize(
        "test_case_id, model,product_service, description, path, port, method, header, params_type,data, json_value,params, file_key, request_file_name, collection_return_data, collect_file, ignore_data, check_data, check_type, exp_data,exp_desc, work_status",
        test_case)  # 参数初始化
    @allure.story("validation")  # story描述
    @allure.suite("{model}")  # suite描述
    @allure.title("No.{test_case_id}-{description}")  # title描述
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.validation
    def test_api_test(self, test_case_id, model, product_service, description, path, port, method, header, params_type,
                      data,
                      json_value,
                      params,
                      file_key, request_file_name, collection_return_data, collect_file, ignore_data, check_data,
                      check_type,
                      exp_data, exp_desc, work_status):
        self.all_num = self.all_num + 1
        if work_status:
            [path, port, headers] = self.handle.get_relation_value(all_data, [path, port, header],
                                                                   ["path", "port", "header"])

            json_value = self.handle.update_validation_data(self.env, json_value, product_service)
            result = self.req.get_request(path, port, method, headers=headers,
                                          json_value=json_value,
                                          file_key=file_key, file_value=request_file_name, timeout=5000)

            if '"code":0' in result:
                self.handle.update_tracking_num(
                    json_value["data"]["packageInfoList"][0][
                        "trackingNumber"])
            assert_result, exp_value, act_value = AssertTool().compare_dict(result, exp_data, ignore_data, check_data)
            exp_1 = "支持" + product_service + "服务" if exp_value[0][0] is True else "不支持" + product_service + "服务"
            self.all_data_list.append(str(json_value).replace("'", '"'))
            self.all_service_list.append(product_service)
            self.all_des_list.append(description + "-" + product_service)
            self.all_file_list.append(description)
            self.all_res_list.append(str(result).replace("'", '"'))
            self.all_exp_list.append(exp_1)
            self.all_assert_list.append(assert_result)
            if assert_result is False:
                # 提取关键信息
                # act_1 = "支持" + product_service + "服务" if act_value[0][0] is True else "不支持" + product_service + "服务"
                self.error_data_list.append(str(json_value).replace("'", '"'))
                self.error_service_list.append(product_service)
                self.error_des_list.append(description + "-" + product_service)
                self.error_file_list.append(description)
                self.error_res_list.append(str(result).replace("'", '"'))
                # self.error_act_list.append(act_1)
                self.error_exp_list.append(exp_1)
                self.error_assert_list.append(assert_result)
                self.error_num += 1
            else:
                self.success_num += 1
            assert assert_result

    def teardown_class(self):
        """
        数据导出
        :return:
        """
        # 生产巡检机器人
        path1 = "/cgi-bin/webhook/send?key=2cff83bf-8d51-4d03-882f-09dffb6cf16d"
        path2 = "/cgi-bin/webhook/upload_media?key=2cff83bf-8d51-4d03-882f-09dffb6cf16d&type=file"
        # lulu机器人
        # path1 = "/cgi-bin/webhook/send?key=474e9964-db83-4cc1-87b3-758be14da3e7"
        # path2 = "/cgi-bin/webhook/upload_media?key=474e9964-db83-4cc1-87b3-758be14da3e7&type=file"
        lulu_robot = WeChat(path1, path2)
        all_data_result = pandas.DataFrame(
            {"路向": self.all_file_list, "服务类型": self.all_service_list, "预期": self.all_exp_list,
             "是否符合预期": self.all_assert_list,
             "请求报文": self.all_data_list,
             "请求结果": self.all_res_list})
        all_data_result.to_excel(
            rootPath + "\\testresults\\resultfile\\validation\\" + self.env + "_validation_" + str(
                DateTimeTool.get_now_time_stamp_with_millisecond()) + "result.xls")
        data_result = pandas.DataFrame(
            {"路向": self.error_file_list, "服务类型": self.error_service_list, "预期": self.error_exp_list,
             "是否符合预期": self.error_assert_list,
             "请求报文": self.error_data_list,
             "请求结果": self.error_res_list})
        error_file = rootPath + "\\testresults\\resultfile\\" + DateTimeTool.get_now_date() + "_" + self.env_desc + "_validation_result.xlsx"
        writer = pandas.ExcelWriter(error_file)
        all_data_result.to_excel(writer, sheet_name="全部测试结果")
        data_result.to_excel(writer, sheet_name="错误数据")
        writer.save()
        beauty_format(error_file)
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **<%s>-巡检测试反馈**\n#### **请注意及时跟进！**\n"
                           "> 接口名称：<font color=\"info\">%s</font> \n"
                           "> 测试用例总数：<font color=\"info\">%s条</font>；测试用例通过率：<font color=\"info\">%s</font>\n"
                           "> **--------------------运行详情--------------------**\n"
                           "> **成功数：**<font color=\"info\">%s</font>\n**失败数：**<font color=\"red\">%s</font>\n" % (
                               self.env_desc, "validation", len(self.all_des_list), "{:.2%}""".format(
                                   (len(self.all_des_list) - len(self.error_des_list)) / len(self.all_des_list)),
                               (len(self.all_des_list) - len(self.error_des_list)), len(self.error_des_list))}}
        data[
            "markdown"][
            "content"] += "> **--------------------错误用例--------------------**\n" if len(
            self.error_des_list) != 0 else "> **--------------------完美通过--------------------**\n"
        for i in self.error_des_list:
            error_record = "> **路向：**<font color=\"warning\">%s</font>\n" % i
            data["markdown"]["content"] += error_record
        data["markdown"]["content"] += "> ##### **具体测试结果详见以下文件**"
        lulu_robot.send_message(data)
        lulu_robot.send_file(error_file)
        self.all_num, self.error_num, self.success_num, self.skip_num = 0, 0, 0, 0
