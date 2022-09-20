# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 17:19
# @File         : resource.py
# @Organization : 成都信息工程大学
# @Description  :


from fastapi import APIRouter, UploadFile, File, Form
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
from api.data_show.parameters import QueryCondition

data_show_router = APIRouter()


@data_show_router.get("/index", name="地图数据展示", description="地图数据展示")
def order_situation_review(request: Request):
    query_result = OriginData.objects(Q(origin_detail__exists=True)
                                      & Q(destination_detail__exists=True)).all()
    origin_data = []
    destination_data = []
    for each_order in query_result:
        origin_data.append({"name": each_order.origin,
                            "lnglat": each_order.origin_detail.lnglat,
                            "style": 0,
                            "utility_type_order_number": each_order.id,
                            "channel_name": each_order.channel_name,
                            "origin": each_order.origin,
                            "destination": each_order.destination,
                            "order_status": each_order.order_status,
                            "order_time": each_order.order_time.strftime("%Y/%m/%d %H:%M"),
                            "order_type": each_order.order_type,
                            "order_way": each_order.order_way,
                            "service_type": each_order.service_type})
        destination_data.append({"name": each_order.destination,
                                 "lnglat": each_order.destination_detail.lnglat,
                                 "style": 1,
                                 "utility_type_order_number": each_order.id,
                                 "channel_name": each_order.channel_name,
                                 "origin": each_order.origin,
                                 "destination": each_order.destination,
                                 "order_status": each_order.order_status,
                                 "order_time": each_order.order_time.strftime("%Y/%m/%d %H:%M"),
                                 "order_type": each_order.order_type,
                                 "order_way": each_order.order_way,
                                 "service_type": each_order.service_type})
    return templates.TemplateResponse("data_show.html",
                                      {"request": request,
                                       "citys_origin": origin_data,
                                       "citys_destination": destination_data,
                                       "start_time": "2022/07/01 00:00",
                                       "end_time": datetime.now().strftime("%Y/%m/%d %H:%M")})


# Request在路径操作中声明一个参数，该参数将返回模板。
# 使用templates您创建的渲染并返回TemplateResponse，并request在Jinja2“上下文” 中将用作键值对之一。
# 基于时间的筛选
# 基于用户的筛选
@data_show_router.post("/order_situation_review", name="地图数据展示", description="地图数据展示")
# def order_situation_review(request: Request, query_condition: QueryCondition):
def order_situation_review(request: Request, start_time: str = Form(title="开始时间"),
                           end_time: str = Form(title="结束时间"),
                           channel_name_1: str = Form(title="主渠道", type=str, default=""),
                           channel_name_2: str = Form(title="微信小程序", type=str, default=""),
                           channel_name_3: str = Form(title="司机端", type=str, default=""),
                           order_way_1: str = Form(title="线上叫单", type=str, default=""),
                           order_way_2: str = Form(title="报单", type=str, default=""),
                           order_status_1: str = Form(title="付款完成", type=str, default=""),
                           order_status_2: str = Form(title="订单取消", type=str, default=""),
                           order_status_3: str = Form(title="确认费用", type=str, default="")):
    query_result = OriginData.objects(Q(origin_detail__exists=True)
                                      & Q(destination_detail__exists=True)
                                      & Q(order_time__gte=datetime.strptime(start_time, "%Y/%m/%d %H:%M"))
                                      & Q(order_time__lte=datetime.strptime(end_time, "%Y/%m/%d %H:%M"))
                                      & Q(channel_name__in=[channel_name_1, channel_name_2, channel_name_3])
                                      & Q(order_way__in=[order_way_1, order_way_2])
                                      & Q(order_status__in=[order_status_1, order_status_2, order_status_3])).all()
    origin_data = []
    destination_data = []
    for each_order in query_result:
        origin_data.append({"name": each_order.origin,
                            "lnglat": each_order.origin_detail.lnglat,
                            "style": 0,
                            "utility_type_order_number": each_order.id,
                            "channel_name": each_order.channel_name,
                            "origin": each_order.origin,
                            "destination": each_order.destination,
                            "order_status": each_order.order_status,
                            "order_time": each_order.order_time.strftime("%Y/%m/%d %H:%M"),
                            "order_type": each_order.order_type,
                            "order_way": each_order.order_way,
                            "service_type": each_order.service_type})
        destination_data.append({"name": each_order.destination,
                                 "lnglat": each_order.destination_detail.lnglat,
                                 "style": 1,
                                 "utility_type_order_number": each_order.id,
                                 "channel_name": each_order.channel_name,
                                 "origin": each_order.origin,
                                 "destination": each_order.destination,
                                 "order_status": each_order.order_status,
                                 "order_time": each_order.order_time.strftime("%Y/%m/%d %H:%M"),
                                 "order_type": each_order.order_type,
                                 "order_way": each_order.order_way,
                                 "service_type": each_order.service_type})
    return templates.TemplateResponse("data_show.html",
                                      {"request": request,
                                       "citys_origin": origin_data,
                                       "citys_destination": destination_data,
                                       "start_time": start_time,
                                       "end_time": end_time})


@data_show_router.get("/origin_data_show/", name="订单数据列表展示", description="订单数据列表展示")
def origin_data_show(request: Request, count: int = 10, pagination: int = 1):
    query_result = OriginData.objects.all()
    data = json.loads(query_result[(pagination - 1) * count:pagination * count].to_json())
    data_count = query_result.count()
    return templates.TemplateResponse("origin_data_show.html", {"request": request,
                                                                "order_list": data,
                                                                "count": data_count,
                                                                "pagination": pagination})


