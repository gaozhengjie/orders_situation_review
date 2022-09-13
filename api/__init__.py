# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 0:42
# @File         : __init__.py
# @Organization : 成都信息工程大学
# @Description  : 初始化前端模板

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
