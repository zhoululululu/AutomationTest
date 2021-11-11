# -*- coding: utf-8 -*- 
"""
Created on 2021/7/7 17:42 
@File  : rdc_flow.py
@author: zhoul
@Desc  :
"""
import random
from case.get_label import GetLabel
import time
from config.config_json_value import ConfigJsonValue
from api.request_client import RequestClient
from config.get_config import Config
from sql.sql_statement import RDCSqlStatement
from commonfunc.sleep_tool import SleepTool
from commonfunc.get_logging import Logging

logger = Logging()


class RdcFlow:
    def __init__(self, env, sortation, service_id, ship_country, battery, tracking_num, vendor_code=None,
                 service_code=None, first_sorting=None, sorting_result=None):
        self.env, self.sortation, self.battery = env, sortation, battery
        self.urls = Config("url").get_urls(env, sortation)
        self.sortation_code = self.urls["sortation_code"]
        self.json_config = ConfigJsonValue(self.env, self.sortation, service_id, ship_country, self.battery,
                                           tracking_num, vendor_code, service_code, first_sorting, sorting_result)
        self.headers = '{"Content-Type": "application/json; charset=UTF-8"}'  # 由于rdc所有的操作都是post-json,直接预设header
        self.bag_id, self.first_sorting_result, self.sorting_result, self.b_post_id, self.last_mile_tracking_number = "", "", "", "", ""
        self.rdc_cursor = RDCSqlStatement(sortation, env)
        self.letter_statue = 0
        self.status = False

    def ship_order(self, order_type, package_total_weight, sku_value, consignee_full_name, consignee_phone,
                   consignee_state,
                   consignee_city, consignee_zipcode, consignee_address1, consignee_address2,
                   txn_value, sku_desc, sku_desc_cn, battery_type, ele_id, letter):
        """
        IS下单
        :param letter:
        :param consignee_phone:
        :param ele_id:
        :param battery_type:
        :param sku_desc_cn:
        :param consignee_zipcode:
        :param sku_desc:
        :param txn_value:
        :param consignee_address2:
        :param consignee_address1:
        :param consignee_city:
        :param consignee_state:
        :param consignee_full_name:
        :param order_type: 请求类型，是需要自定义还是
        :param package_total_weight: 包裹重量
        :param sku_value: 商品申报金额
        :return:
        """
        if order_type in ("only_order", "rdc_order"):
            re_tracking_number, ship_order_data, weight, letter = self.json_config.get_ship_order_data(
                package_total_weight,
                sku_value, consignee_full_name, consignee_phone, consignee_state, consignee_city,
                consignee_zipcode, consignee_address1, consignee_address2, txn_value, sku_desc,
                sku_desc_cn,
                battery_type,
                ele_id, letter)
        elif order_type == "sorting_order":
            re_tracking_number, ship_order_data, weight, battery_type, letter = self.json_config.get_ship_order_data_with_sorting()
        if letter:
            self.letter_statue = 1
        try:
            ship_order_response = RequestClient(self.urls["ship_order"]).get_simple_request("post", ship_order_data,
                                                                                            headers=self.headers)

            logger.info("IS下单订单 : %s" % re_tracking_number)
            logger.info("IS下单入参 : %s" % ship_order_data)
            logger.info("IS下单结果 : %s" % ship_order_response)
        finally:
            return re_tracking_number, weight, battery_type, letter

    def get_letter(self):
        """
        打标
        :return:
        """
        re_tracking_number, letter_data = self.json_config.get_letter_data(self.sortation_code)
        get_letter_response = RequestClient(self.urls["get_letter"]).get_simple_request("post", letter_data,
                                                                                        headers=self.headers)

        logger.info("打标订单 : %s" % re_tracking_number)
        logger.info("打标入参 : %s" % letter_data)
        logger.info("打标结果 : %s" % get_letter_response)

    def get_label(self, package_weight):
        """
        换单
        :param package_weight:
        :return:
        """
        re_tracking_number, label_data = self.json_config.get_label_data(self.sortation_code, package_weight)
        try:
            get_label_response = RequestClient(self.urls["get_label"]).get_simple_request("post", label_data,
                                                                                          headers=self.headers,
                                                                                          timeout=999999)

            logger.info("换单订单 : %s" % re_tracking_number)
            logger.info("换单入参 : %s" % label_data)
            logger.info("换单结果 : %s" % get_label_response)

            # 还需要对结果进行收集，收集first_sorting_result,sorting_result,last_mile_tracking_number等(后续流程需要)
            if self.sortation == "dg":
                self.first_sorting_result = get_label_response["result"]["firstSortingResult"]
                self.sorting_result = get_label_response["result"]["sortingResult"]
                self.last_mile_tracking_number = get_label_response["result"]["lastmileTrackingNumber"]
            else:
                self.first_sorting_result = get_label_response["data"]["firstSortingResult"]
                self.sorting_result = get_label_response["data"]["sortingResult"]
                self.last_mile_tracking_number = get_label_response["data"]["lastmileTrackingNumber"]

            logger.info("收集参数 : {firstSortingResult: %s }" % self.first_sorting_result)
            logger.info("收集参数 : {sortingResult:%s }" % self.sorting_result)
            logger.info("收集参数 : {lastmileTrackingNumber: %s }" % self.last_mile_tracking_number)
        except Exception as e:
            if get_label_response["errors"]["message"]:
                self.last_mile_tracking_number = get_label_response["errors"]["message"]
            else:
                self.last_mile_tracking_number = "error"
            logger.error("请求错误 : %s" % e)
        finally:
            return self.last_mile_tracking_number

    def get_b_post(self):
        b_post = self.json_config.get_b_post_data(self.sortation_code)
        get_b_post_response = ""
        try:
            get_b_post_response = RequestClient(self.urls["get_last_mile_bag"]).get_simple_request("post", b_post,
                                                                                                   headers=self.headers)

            logger.info("获取比邮号入参 : %s" % b_post)
            logger.info("获取比邮号结果 : %s" % get_b_post_response)
        except Exception as e:
            get_b_post_response = "error"
            logger.error("请求错误 : %s" % e)
        finally:
            return get_b_post_response

    def bu_bag(self, bag_real_weight):
        """
        建包; 需要分拣后的初分垛口，细分垛口，尾程面单号
        :param bag_real_weight:
        :return:
        """
        bu_bag_data, status = self.json_config.get_bu_bag_data(self.sortation_code, bag_real_weight,
                                                               self.first_sorting_result,
                                                               self.sorting_result,
                                                               self.last_mile_tracking_number)
        if status == "b_post":
            logger.info("该订单需要获取比邮号，准备进行比邮大包号获取")
            b_post_data = self.get_b_post()["data"]["lastMileBagIdStart"]
            logger.info("获取比邮号入参 : %s" % b_post_data)
            bu_bag_data["data"]["lastMileBagId"] = b_post_data
        elif status == "k_post":
            logger.info("该订单需要获取皇邮号，准备赋值皇邮号")
            bu_bag_data["data"]["lastMileBagId"] = str(random.randint(1000, 9999)) + "PPYVR" + str(
                random.randint(100000, 999999))
        try:
            bu_bag_response = RequestClient(self.urls["bu_bag"]).get_simple_request("post", bu_bag_data,
                                                                                    headers=self.headers)
            logger.info("建包订单 : %s" % self.last_mile_tracking_number)
            logger.info("建包入参 : %s" % bu_bag_data)
            logger.info("建包结果 : %s" % bu_bag_response)
            # 收集bag_id信息啦,准备负重出库！
            if self.sortation == "dg":
                self.bag_id = bu_bag_response["data"]["bagId"]
            else:
                self.bag_id = bu_bag_response["data"]["bagId"]
        except Exception as e:
            if bu_bag_response["errors"][0]["message"]:
                self.bag_id = bu_bag_response["errors"][0]["message"]
            else:
                self.bag_id = "error"
            logger.error("请求错误 : %s" % e)
        finally:
            return self.bag_id

    def real_weight(self, bag_real_weight):
        """
        负重; 需要建包后的bag_id
        :param bag_real_weight: 实际重量
        :return:
        """
        if self.sortation == "dg":
            real_weight_data = self.json_config.get_bag_weight_data(bag_real_weight, self.bag_id)
            try:
                real_weight_response = RequestClient(self.urls["bag_weight"]).get_simple_request("post",
                                                                                                 real_weight_data,
                                                                                                 headers=self.headers)
                logger.info("负重订单 : %s" % self.bag_id)
                logger.info("负重入参 : %s" % real_weight_data)
                logger.info("负重结果 : %s" % real_weight_response)
            except Exception as e:
                logger.error("请求错误 : %s" % e)
        else:
            logger.info("嘉兴订单无需负重")
            pass

    def out_package(self):
        """
        出库
        :return:
        """
        out_package_data = self.json_config.get_out_package_data(self.bag_id)
        try:
            out_package_response = RequestClient(self.urls["out_package"]).get_simple_request("post", out_package_data,
                                                                                              headers=self.headers)
            logger.info("出库订单 : %s" % self.bag_id)
            logger.info("出库入参 : %s" % out_package_data)
            logger.info("出库结果 : %s" % out_package_response)

        except Exception as e:
            logger.error("请求错误 : %s" % e)


def get_rdc_interface(order_type, data_list):
    tracking_list, last_tracking_list, result, bag_list, single_result, only_order_result, letter_list, weight_list, country_list, service_code_list, vendor_code_list, sorting_result_list, first_sorting_list, rdc_list, env_list, service_list, battery_list = [], [], [], [], {}, [], [], [], [], [], [], [], [], [], [], [], []
    for i in data_list:
        env, rdc, service, country, vendor_code, service_code, first_sorting, sorting_result, package_total_weight, sku_value, consignee_full_name, consignee_phone, consignee_state, consignee_city, consignee_zipcode, consignee_address1, consignee_address2, txn_value, sku_desc, sku_desc_cn, battery_type, ele_id, letter = i.get(
            "env"), i.get("rdc"), i.get("service"), i.get("country"), i.get("vendor_code"), i.get(
            "service_code"), i.get("first_sorting"), i.get("sorting_result"), i.get("weight"), i.get(
            "sku_value"), i.get(
            "consignee_full_name"), i.get(
            "consignee_phone"), i.get("consignee_state"), i.get("consignee_city"), i.get(
            "consignee_zipcode"), i.get("consignee_address1"), i.get("consignee_address2"), i.get(
            "txn_value"), i.get("sku_desc"), i.get(
            "sku_desc_cn"), i.get("battery"), i.get("ele_id"), i.get("letter")
        rdc_flow = RdcFlow(env, rdc, service, country, battery_type, "", vendor_code,
                           service_code, first_sorting, sorting_result)
        tracking_number, weight, battery_type, letter_status = rdc_flow.ship_order(order_type, package_total_weight,
                                                                                   sku_value,
                                                                                   consignee_full_name,
                                                                                   consignee_phone, consignee_state,
                                                                                   consignee_city, consignee_zipcode,
                                                                                   consignee_address1,
                                                                                   consignee_address2,
                                                                                   txn_value, sku_desc, sku_desc_cn,
                                                                                   battery_type,
                                                                                   ele_id,
                                                                                   letter)
        env_list.append(env)
        rdc_list.append(rdc)
        service_list.append(service)
        battery_list.append(battery_type)
        tracking_list.append(tracking_number)
        vendor_code_list.append(vendor_code)
        service_code_list.append(service_code)
        first_sorting_list.append(first_sorting)
        sorting_result_list.append(sorting_result)
        country_list.append(country)
        weight_list.append(weight)
        letter_list.append(letter_status)
        single_result["country"] = i.get("country")
        single_result["tracking_number"] = tracking_number
        only_order_result.append(single_result)
        single_result = {}
    if order_type == "only_order":
        return only_order_result
    else:
        for i in data_list:
            single_result["country"] = country_list[data_list.index(i)]
            single_result["tracking_number"] = tracking_list[data_list.index(i)]
            rdc_flow = RdcFlow(env_list[data_list.index(i)], rdc_list[data_list.index(i)],
                               service_list[data_list.index(i)], country_list[data_list.index(i)],
                               battery_list[data_list.index(i)], tracking_list[data_list.index(i)],
                               vendor_code_list[data_list.index(i)], service_code_list[data_list.index(i)],
                               first_sorting_list[data_list.index(i)], sorting_result_list[data_list.index(i)])
            status = SleepTool.wait_for_tracking_number(rdc_list[data_list.index(i)], env_list[data_list.index(i)],
                                                        tracking_list[data_list.index(i)])
            if status is True:
                logger.info("******************IS同步订单至RDC成功******************")
                if letter_list[data_list.index(i)] == 1:
                    print("该订单需要打标")
                    rdc_flow.get_letter()
                last_mile_tracking_number = rdc_flow.get_label(weight_list[data_list.index(i)])
                single_result["last_mile_tracking_number"] = last_mile_tracking_number
                last_tracking_list.append(last_mile_tracking_number)
                time.sleep(1)
                act_service_code, label = GetLabel(env_list[data_list.index(i)], rdc_list[data_list.index(i)],
                                                   tracking_list[data_list.index(i)]).get_label()
                bag_id = rdc_flow.bu_bag(weight_list[data_list.index(i)])
                if bag_id != "error":
                    single_result["bag_id"] = bag_id
                    bag_list.append(bag_id)
                    rdc_flow.real_weight(weight_list[data_list.index(i)])
                    rdc_flow.out_package()
                else:
                    single_result["bag_id"] = bag_id
            else:
                single_result["error"] = "订单同步失败，请检查订单"
                logger.info("订单同步失败，请检查订单")

            single_result["sdk_label"] = label
            single_result["exp_service_code"] = service_code_list[data_list.index(i)]
            single_result["act_service_code"] = act_service_code
            single_result["assert"] = act_service_code == service_code_list[data_list.index(i)]

            result.append(single_result)
            single_result = {}
        return result
