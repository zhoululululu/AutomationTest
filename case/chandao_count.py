# -*- coding: utf-8 -*- 
"""
Created on 2021/11/9 16:03 
@File  : chandao_count.py
@author: zhoul
@Desc  :
"""
from PIL import Image
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
from commonfunc.datetime_tool import DateTimeTool
import os
from config.get_config import Config
from commonfunc.wx_robot import WeChat

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class ChanDaoCount(object):
    def __init__(self):
        self.c = Config("ui_xpath").get_ui_xpath()
        self.bug_pic, self.bug_assign, self.no_1_assign, self.no_1_bugs, self.total_num = "", "", "", "", ""

    @staticmethod
    def open_chrome(url):
        '''
        初始化driver，打开页面
        '''
        # 适配chrome_driver
        chrome_driver = "E:/chromedriver/chromedriver"
        driver = webdriver.Chrome(chrome_driver)
        driver.maximize_window()
        driver.get(url)
        return driver

    def get_count(self, url):
        driver = self.open_chrome(url)
        driver.find_element_by_xpath(self.c["account"]).send_keys("181471")
        driver.find_element_by_xpath(self.c["password"]).send_keys("zhoulu@123")
        driver.find_element_by_xpath(self.c["submit"]).click()
        time.sleep(1)
        driver.find_element_by_xpath(self.c["qa"]).click()
        driver.find_element_by_xpath(self.c["product"]).click()
        time.sleep(2)
        driver.find_element_by_xpath(self.c["spk"]).click()
        time.sleep(2)
        driver.find_element_by_xpath(self.c["search_tab"]).click()
        time.sleep(1)
        s1 = Select(driver.find_element_by_id('queryID'))  # 实例化Select
        time.sleep(1)
        s1.select_by_value("165")
        time.sleep(2)
        driver.find_element_by_xpath(self.c["search_submit"]).click()
        time.sleep(2)
        driver.find_element_by_xpath(self.c["choose_range_before"]).click()
        time.sleep(2)
        driver.find_element_by_xpath(self.c["choose_range"]).click()
        time.sleep(2)
        self.total_num = driver.find_element_by_xpath(self.c["total_num"]).text
        # 第一波截图
        js_bottom = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js_bottom)
        file_name_1 = rootPath + "\\testresults\\bug\\bugpic\\" + DateTimeTool.get_now_date() + "bug_1" + ".png"
        self.bug_pic = rootPath + "\\testresults\\bug\\bugpic\\" + DateTimeTool.get_now_date() + "_bug" + ".png"
        driver.get_screenshot_as_file(file_name_1)
        self.cut_pic(file_name_1, self.bug_pic, 230, 98, 1920, 925)
        time.sleep(4)
        driver.find_element_by_xpath(self.c["report_btn"]).click()
        time.sleep(2)
        driver.find_element_by_xpath(self.c["assign_by"]).click()
        time.sleep(2)
        driver.find_element_by_xpath(self.c["generate_report"]).click()
        time.sleep(2)
        js_bottom = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js_bottom)
        file_name_1 = rootPath + "\\testresults\\bug\\assignpic\\" + DateTimeTool.get_now_date() + "_assign_1" + ".png"
        self.bug_assign = rootPath + "\\testresults\\bug\\assignpic\\" + DateTimeTool.get_now_date() + "_assign" + ".png"
        driver.get_screenshot_as_file(file_name_1)
        self.cut_pic(file_name_1, self.bug_assign, 280, 170, 1900, 650)
        time.sleep(3)
        self.no_1_assign = driver.find_element_by_xpath(self.c["no1_assign"]).text
        self.no_1_bugs = driver.find_element_by_xpath(self.c["no1_bugs"]).text
        driver.quit()

    @staticmethod
    def cut_pic(file, file2, i, j, k, g):
        # 读取图片
        img_1 = Image.open(file)
        # 设置裁剪的位置
        crop_box = (i, j, k, g)
        # 裁剪图片
        img_2 = img_1.crop(crop_box)
        img_2.save(file2)

    def robot_send(self, url):
        self.get_count(url)
        path1 = "/cgi-bin/webhook/send?key=d91abfc9-774d-462a-8db2-6324646bce4c"
        path2 = "/cgi-bin/webhook/upload_media?key=d91abfc9-774d-462a-8db2-6324646bce4c&type=file"
        lulu_robot = WeChat(path1, path2)
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **禅道未关闭BUG反馈**\n#### **请注意及时跟进！**\n"
                           "> 日期：<font color=\"info\">%s</font> \n"
                           "> BUG总数：<font color=\"info\">%s条</font> \n"
                           "> BUG指派第1名：<font color=\"red\">%s</font> \n" % (
                               DateTimeTool.get_now_date(), self.total_num, self.no_1_assign)}}
        data["markdown"]["content"] += "> **--------------------------------------------**\n"
        data["markdown"]["content"] += "> ##### **具体内容详见以下图片**"
        lulu_robot.send_message(data)
        lulu_robot.send_image(self.bug_pic)
        lulu_robot.send_image(self.bug_assign)


if __name__ == '__main__':
    ChanDaoCount().robot_send("http://project.itiaoling.com/zentao/user-login.html")
    # ChanDaoCount().cut_pic(rootPath + "\\testresults\\bug\\assignpic\\2021-11-29bug_1.png",
    #                        rootPath + "\\testresults\\bug\\assignpic\\2021-11-29_assign.png", 280, 170, 1900, 650)
