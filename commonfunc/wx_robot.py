# -*- coding: utf-8 -*- 
"""
Created on 2021/9/13 13:53 
@File  : wx_robot.py
@author: zhoul
@Desc  :
"""

from api.request_client import RequestClient
import os
import hashlib
import base64

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class WeChat:

    def __init__(self, path1, path2):
        self.request = RequestClient("https://qyapi.weixin.qq.com")
        self.header = '{"Content-Type": "application/json"}'
        self.path1 = path1
        self.path2 = path2
        # self.path1 = "/cgi-bin/webhook/send?key=2cff83bf-8d51-4d03-882f-09dffb6cf16d"
        # self.path2 = "/cgi-bin/webhook/upload_media?key=2cff83bf-8d51-4d03-882f-09dffb6cf16d&type=file"
        # self.path1 = "/cgi-bin/webhook/send?key=474e9964-db83-4cc1-87b3-758be14da3e7"
        # self.path2 = "/cgi-bin/webhook/upload_media?key=474e9964-db83-4cc1-87b3-758be14da3e7&type=file"

    @staticmethod
    def message(env, project, total, passing, succeed, failing, error_list):
        """
        需要发送到企业微信的文案信息
        :param env:             环境
        :param project:         项目名称
        :param total:           总计
        :param passing:         通过率
        :param succeed:         通过数
        :param failing:         失败数
        :param skip:            跳过数
        :param error:           错误数
        :param error_list:     错误例子
        :param file:            测试文件
        :return:                返回data信息
        """
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **<%s>-巡检测试反馈**\n#### **请注意及时跟进！**\n"
                           "> 接口名称：<font color=\"info\">%s</font> \n"
                           "> 测试用例总数：<font color=\"info\">%s条</font>；测试用例通过率：<font color=\"info\">%s</font>\n"
                           "> **--------------------运行详情--------------------**\n"
                           "> **成功数：**<font color=\"info\">%s</font>\n**失败数：**<font color=\"red\">%s</font>\n" % (
                               env, project, total, passing, succeed, failing)}}
        data[
            "markdown"][
            "content"] += "> **--------------------错误用例--------------------**\n" if failing != 0 else "> **--------------------完美通过--------------------**\n"
        for i in error_list:
            error_record = "> **路向：**<font color=\"warning\">%s</font>\n" % i
            data["markdown"]["content"] += error_record
            print(data["markdown"]["content"])
        data["markdown"]["content"] += "> ##### **具体测试结果详见以下文件**"

        return data

    def send_message(self, send_result_data):
        """
        发送文案信息
        :param send_result_data:   请求文件
        :return:
        """
        # 获取企业微信群机器人的url, 使用的python第三方库requests库发送的请求
        # 发送请求报告
        res = self.request.get_request(path=self.path1, port="", method="post", json_value=send_result_data,
                                       headers=self.header,
                                       file_value='')

    def send_file(self, file):
        """
        发送文案信息
        :param file:            文件
        :return:
        """
        # 获取企业微信群机器人的url, 使用的python第三方库requests库发送的请求
        # # 上传测试报告文件
        media_id = self.request.get_request(path=self.path2, port="", method="post", json_value="{}",
                                            headers=self.header,
                                            file_value=file, file_key="file")['media_id']
        #
        send_file_data = {"msgtype": "file", "file": {"media_id": media_id}}
        # # 发送测试报告文件
        send_file = self.request.get_request(path=self.path1, port="", method="post", json_value=send_file_data,
                                             headers=self.header,
                                             file_value='')

        return send_file

    def send_image(self, image):
        """
        :param image:        图片
        :return:
        """
        with open(image, 'rb') as file:  # 转换图片成base64格式
            data = file.read()
            encode_str = base64.b64encode(data)
            image_data = str(encode_str, 'utf-8')

        with open(image, 'rb') as file:  # 图片的MD5值
            md = hashlib.md5()
            md.update(file.read())
            image_md5 = md.hexdigest()
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "image",
            "image": {
                "base64": image_data,
                "md5": image_md5
            }
        }

        result = self.request.get_request(path=self.path1, port="", method="post", json_value=data,
                                          headers=headers,
                                          file_value='')
        return result
