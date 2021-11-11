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

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class ChanDaoCount(object):
    def __init__(self):
        self.c = {
            'account': '//input[contains(@name,"account")]',
            'password': '//input[contains(@name,"password")]',
            'submit': '//button[contains(@type,"submit")]',
            'qa': '//li[contains(@data-id,"qa")]',
            'search_tab': '//li[contains(@id,"bysearchTab")]',
            'product': '//span[contains(@class,"icon-caret-down")]',
            'spk': '//a[contains(text()," SpeedPAK")]',
            'query_box': '//span[contains(@id,"queryBox")]',
            'search_select': '//select[contains(@name,"queryID")]',
            'search_submit': '//button[contains(text(),"搜索")]',
            'choose_range_before': '//a[contains(text(),"每页")]',
            'choose_range': '//*[@id="bugList"]/tfoot/tr/td/div[2]/div/div/ul/li[11]/a'  # 感觉定位不到，因为这个内容八成是不会变的，所以就先这样
        }

    @staticmethod
    def open_chrome(url):
        '''
        初始化driver，打开页面
        '''
        # 适配chrome_driver
        chrome_driver = "E:/chromedriver/chromedriver"
        driver = webdriver.Chrome(chrome_driver)
        # driver.set_window_size(500, 600)
        driver.maximize_window()
        driver.get(url)
        return driver

    def sleep_for_element(self, element):
        pass

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
        # 第一波截图
        js_bottom = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js_bottom)
        file_name_1 = rootPath + "\\testresults\\bug\\bugpic\\" + DateTimeTool.get_now_date() + "-bug截图" + ".png"
        driver.get_screenshot_as_file(file_name_1)
        self.cut_pic(file_name_1)
        time.sleep(2)
        # driver.quit()

    @staticmethod
    def cut_pic(file, file2):
        # 读取图片
        img_1 = Image.open(file)
        # 设置裁剪的位置
        crop_box = (10, 10, 0, 0)
        # 裁剪图片
        img_2 = img_1.crop(crop_box)
        img_2.save(file2)


if __name__ == '__main__':
    # ChanDaoCount().get_count("http://project.itiaoling.com/zentao/user-login.html")
    ChanDaoCount().cut_pic(rootPath + "\\testresults\\bug\\bugpic\\" + "2021-11-09-bug.png",
                           rootPath + "\\testresults\\bug\\bugpic\\" + "2021-11-09-bug截图_1.png")
