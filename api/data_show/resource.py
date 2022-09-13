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
    data = []
    for each_order in query_result:
        data.append({"name": each_order.origin,
                     "lnglat": each_order.origin_detail.lnglat,
                     "style": 0})
        data.append({"name": each_order.destination,
                     "lnglat": each_order.destination_detail.lnglat,
                     "style": 1})
    return templates.TemplateResponse("data_show.html",
                                      {"request": request,
                                       "citys": data,
                                       "start_time": "2022-07-01 00:00:00",
                                       "end_time": "9999-07-01 00:00:00"})


# Request在路径操作中声明一个参数，该参数将返回模板。
# 使用templates您创建的渲染并返回TemplateResponse，并request在Jinja2“上下文” 中将用作键值对之一。
# 基于时间的筛选
# 基于用户的筛选
@data_show_router.post("/order_situation_review", name="地图数据展示", description="地图数据展示")
# def order_situation_review(request: Request, query_condition: QueryCondition):
def order_situation_review(request: Request, start_time: datetime = Form(title="开始时间"),
                           end_time: datetime = Form(title="结束时间"),
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
                                      & Q(order_time__gte=start_time)
                                      & Q(order_time__lte=end_time)
                                      & Q(channel_name__in=[channel_name_1, channel_name_2, channel_name_3])
                                      & Q(order_way__in=[order_way_1, order_way_2])
                                      & Q(order_status__in=[order_status_1, order_status_2, order_status_3])).all()
    data = []
    for each_order in query_result:
        data.append({"name": each_order.origin,
                     "lnglat": each_order.origin_detail.lnglat,
                     "style": 0})
        data.append({"name": each_order.destination,
                     "lnglat": each_order.destination_detail.lnglat,
                     "style": 1})
    return templates.TemplateResponse("data_show.html",
                                      {"request": request,
                                       "citys": data,
                                       "start_time": start_time,
                                       "end_time": end_time})
