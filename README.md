# 订单复盘分析
## 功能描述
用于代驾订单复盘，辅助老胡的日常分析工作

## 实现方法
- 前后端不分离（因为分离的我不会）
- 后端采用的fastapi
- jinja2渲染前端页面
- 数据库mongodb

## TODO
- 增加文件上传接口，数据上传后后台自动实现地点的经纬度信息补全（目前是通过doc手动进行）
- 红色点代表起点，蓝色点代表终点，在界面上增加图例的说明
- 不同类型的点基于js添加事件联动，根据类型的选择可以隐藏或显示点
- 点击某一个点查看具体详情
    - 主要是显示该条订单的相关属性信息
    - 同时起点和终点之间可以考虑通过虚曲线连接
- 时间筛选条件那儿做一个时间选择器

## 联系
gaozhengj@foxmail.com