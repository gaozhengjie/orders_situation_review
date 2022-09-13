# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 0:11
# @File         : v1_router.py
# @Organization : 成都信息工程大学
# @Description  : 帮助老胡对代驾的订单数据进行复盘分析

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mongoengine import connect, disconnect
from router.v1_router import api_v1_router

from starlette.staticfiles import StaticFiles

app = FastAPI()
app.include_router(api_v1_router)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongodb_info = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'orders_situation_review'
}


# 启动服务的同时调用该函数
@app.on_event("startup")
async def connect_mongodb():
    connect(**mongodb_info)
    print("数据库连接成功")


# 关闭服务的同时调用该函数
@app.on_event("shutdown")
async def disconnect_mongodb():
    disconnect()
    print("数据库关闭成功")


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, debug=False)
