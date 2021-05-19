# -*- coding: utf-8 -*-
# @File  : faker.py
# @Author: 周璐
# @Date  : 2021/5/19 22:46
# @Desc  :


import random
import string

from faker.proxy import Faker

fake = Faker(locale='zh_CN')


class Faker(Faker):
    # 随机生成人名
    @classmethod
    def get_person_name(cls):
        name = fake.name()
        return name

    # 随机生成身份证号
    @classmethod
    def get_id_no(cls):
        id_no = fake.ssn()
        return id_no

    # 随机生成手机号
    @classmethod
    def get_phone_no(cls):
        phone = fake.phone_number()
        return phone

    # 随机生成邮箱地址
    @classmethod
    def get_email(cls):
        email = fake.email()
        return email

    # 随机生成省份
    @classmethod
    def get_province(cls):
        province = fake.province()
        return province

    # 随机生成地址 eg：海南省上海市朝阳邱路y座 175208
    @classmethod
    def get_address(cls):
        address = fake.address()
        return address

    # 随机生成三位数
    @classmethod
    def get_three_no(cls):
        three_number = fake.random_number(digits=3)
        return three_number

    @classmethod
    def appoint_random_str_5000(cls):
        """
        生成一个指定长度的随机字符串，其中
        string.digits=0123456789
        string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(5000)]
        random_str = ''.join(str_list)
        return random_str

    @classmethod
    def appoint_random_str_5001(cls):
        """
        生成一个指定长度的随机字符串，其中
        string.digits=0123456789
        string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(5001)]
        random_str = ''.join(str_list)
        return random_str


if __name__ == '__main__':
    print(Faker.get_address())
