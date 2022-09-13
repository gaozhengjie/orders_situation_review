# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 0:16
# @File         : resource.py
# @Organization : 成都信息工程大学
# @Description  : 数据接入

from fastapi import APIRouter, UploadFile, File
from starlette.requests import Request
from api import templates
from utils.response import Response
from db.model import OriginData, AddressInfo
from datetime import datetime
from tqdm import tqdm
from mongoengine.errors import ValidationError
import requests
import json
from mongoengine.queryset.visitor import Q

data_access_router = APIRouter()


def get_addr_detail(abbreviated_address):
    """
    获取地址详细信息
    :param abbreviated_address: 缩写地址
    :return:
    """
    kv = {"key": "6ac3e7964c60f1042f9c350a6e6287c0",
          "keywords": abbreviated_address,
          "city": "成都",
          "citylimit": True,
          "children": 1,
          "offset": 1,
          "page": 1,
          "extensions": "all"}
    r = requests.request("GET", "http://restapi.amap.com/v3/place/text", params=kv)
    parse_result = {}
    if r.status_code == 200:
        response_data = json.loads(r.text)
        if len(response_data.get("pois", [])) > 0:  # 查询到了数据  # fixme: 后期可以考虑换成地理编码接口
            parse_result["lnglat"] = response_data["pois"][0]["location"].split(",")
            tmp_addr = abbreviated_address if len(response_data["pois"][0]["address"]) == 0 \
                else response_data["pois"][0]["address"]
            parse_result["address"] = tmp_addr if response_data["pois"][0]["adname"] in tmp_addr \
                else response_data["pois"][0]["adname"] + tmp_addr
            parse_result["business_area"] = response_data["pois"][0]["business_area"] if isinstance(
                response_data["pois"][0]["business_area"], str) else ""
            parse_result["adname"] = response_data["pois"][0]["adname"]
    return parse_result


@data_access_router.get("/get_lng_lat", name="获取数据的经纬度", description="获取数据的经纬度")
def get_lng_lat():
    # data = OriginData.objects(Q(origin_detail__exists=False) | Q(destination_detail__exists=False)).all()
    data = OriginData.objects(order_time__gte="2022-09-01").all()
    for idx, each_order in enumerate(tqdm(data, desc="补全地址")):
        # 判断源地址是否已经解析
        if each_order.origin_detail is None:
            origin = each_order.origin
            origin_detail = get_addr_detail(origin)
            if len(origin_detail) != 0:
                each_order.origin_detail = AddressInfo(**origin_detail)
                each_order.save()
        # 判断目的地址是否已经解析
        if each_order.destination_detail is None:
            destination = each_order.destination
            destination_detail = get_addr_detail(destination)
            if len(destination_detail) != 0:
                each_order.destination_detail = AddressInfo(**destination_detail)
                each_order.save()
    return Response()


@data_access_router.post("/upload_data", name="导入数据", description="上传需要分析的csv文件")
async def upload_data(file: UploadFile):  # fixme: 版本原因，该版本pydantic不支持UploadFile类型，需要实例化
    content = await file.read()
    try:
        order_list = list(
            map(lambda x: x.split(","),
                str(content, "GBK").strip().splitlines()))  # 转化为字符串格式后一定要strip一下，否则split后会得到最后空白元素
    except UnicodeDecodeError as _:
        if "\ufeff" in str(content, "utf-8"):
            order_list = list(map(lambda x: x.split(","), str(content, "utf-8-sig").strip().splitlines()))
        else:
            order_list = list(map(lambda x: x.split(","), str(content, "utf-8").strip().splitlines()))

    # 数据映射
    csv_header2db_key = {"订单类型": "order_type",
                         "实效类型/订单号": "utility_type_order_number",
                         "渠道订单号": "channel_order_number",
                         "渠道名称": "channel_name",
                         "下单类型": "order_way",
                         "订单状态": "order_status",
                         "下单时间": "order_time",
                         "预约时间": "appointment_time",
                         "完成时间": "completion_time",
                         "出发地": "origin",
                         "目的地": "destination",
                         "服务类型": "service_type",
                         "运力公司": "transport_company",
                         "司机编号": "driver_number",
                         "司机姓名": "driver_name",
                         "司机电话": "driver_telephone",
                         "客户姓名": "customer_name",
                         "客户电话": "customer_telephone",
                         "订单总金额": "order_amount",
                         "退款金额": "refund_amount",
                         "赔付金额": "reparation_amount"}
    header = []
    for idx, each_order in enumerate(tqdm(order_list, desc="导入数据")):
        if idx == 0:  # 第1行，表头，验证表格式是否正确
            if set(each_order) == set(csv_header2db_key.keys()):
                header = each_order
                continue
            else:
                return Response(info="表格式不正确，请仔细核对表头",
                                code=0)
        else:
            tmp = {}
            for key, value in zip(header, each_order):
                if csv_header2db_key[key] in ["order_time", "appointment_time", "completion_time"]:
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    except ValueError as _:
                        if value == "":
                            value = None
                        else:
                            return Response(info="{}字段的时间格式有误，请仔细核对".format(key),
                                            code=0)
                if key == "实效类型/订单号":
                    value = value.split("/")[-1]
                tmp[csv_header2db_key[key]] = value
            try:
                OriginData(**tmp).save()
            except ValidationError as _:  # 数据校验失败，直接跳过该条数据
                pass

    return Response()
