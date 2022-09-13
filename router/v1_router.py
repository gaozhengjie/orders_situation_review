# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 0:11
# @File         : v1_router.py
# @Organization : 成都信息工程大学
# @Description  : 路由配置

from api.data_access.resource import data_access_router
from api.data_show.resource import data_show_router
from fastapi import APIRouter

api_v1_router = APIRouter()

api_v1_router.include_router(data_access_router, tags=["数据接入"])
api_v1_router.include_router(data_show_router, tags=["数据展示"])
