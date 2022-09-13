# -*- coding: utf-8 -*-
# @Author       : 高正杰
# @Email        : gaozhengj@foxmail.com
# @Date         : 2022/8/3 0:16
# @File         : model.py
# @Organization : 成都信息工程大学
# @Description  : 数据库原型声明

from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, DateTimeField, ListField


class AddressInfo(EmbeddedDocument):
    lnglat = ListField(StringField())  # 经纬度
    address = StringField()  # 补全的地址，包括区、街道、门牌号等
    business_area = StringField()  # 所属商务区？主要是针对天府新区和高新区这样的功能区，本身还有自己的行政区
    adname = StringField()  # 行政区


class OriginData(Document):
    order_type = StringField()
    utility_type_order_number = StringField(primary_key=True)
    channel_order_number = StringField()
    channel_name = StringField()
    order_way = StringField()
    order_status = StringField()
    order_time = DateTimeField(default=None)
    appointment_time = DateTimeField(default=None)
    completion_time = DateTimeField(default=None)
    origin = StringField()
    destination = StringField()
    service_type = StringField()
    transport_company = StringField()
    driver_number = StringField()
    driver_name = StringField()
    driver_telephone = StringField()
    customer_name = StringField()
    customer_telephone = StringField()
    order_amount = StringField()
    refund_amount = StringField()
    reparation_amount = StringField()
    origin_detail = EmbeddedDocumentField(AddressInfo)
    destination_detail = EmbeddedDocumentField(AddressInfo)
