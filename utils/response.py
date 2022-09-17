# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 0:54
# @File         : response.py
# @Organization : 成都信息工程大学
# @Description  : 包装响应体

from pydantic import BaseModel, Field


class Response(BaseModel):
    info: str = Field(title="返回信息", default="请求成功")
    code: int = Field(title="返回代码", default=1, description="1表示正常，0表示异常")


class ResponseData(Response):
    data: list = Field(title="返回数据", default=[])


class ResponseDataWithPagination(ResponseData):
    count: int = Field(title="数据总条数", default=0)
    pagination: int = Field(title="总页码", default=1)
