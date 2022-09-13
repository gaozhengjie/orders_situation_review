# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 23:28
# @File         : parameters.py
# @Organization : 成都信息工程大学
# @Description  :


from pydantic import BaseModel, Field
from datetime import datetime


class QueryCondition(BaseModel):
    start_time: datetime = Field(title="开始时间", default="2000-01-01 00:00:00")
    end_time: datetime = Field(title="结束时间", default=datetime.now())
