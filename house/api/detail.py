from flask import Blueprint, request, jsonify, Response
from models import House
from sqlalchemy import func
from datetime import datetime,timedelta


detail_api = Blueprint('detail_api', __name__)

#户型占比，饼图
@detail_api.route('/piedata/<block>',methods=['post'])
def pie_data(block):
    print(block)
    result = House.query.with_entities(House.rooms,func.count()).filter(House.block == block).group_by(House.rooms).order_by(func.count().desc()).all()
    data = []
    for item in result:
        data.append({ 'name': item[0],'value': item[1]})
    return jsonify({'code': '1', 'msg': '查询出来','data':data})

#房源Top20 柱状图
@detail_api.route('/columndata/<block>', methods=['post'])
def column_data(block):
    result = House.query.with_entities(House.address, func.count()).filter(House.block == block).group_by(House.address).order_by(func.count().desc()).limit(20).all()
    name = []
    list = []
    for addr, num in result:
        # 提取地区名，去掉 - 分隔后的后半部分
        addr_name = addr.rsplit('-', 1)[1]
        name.append(addr_name)
        list.append(num)

    data = {
        'name': name,
        'list': list
    }
    return jsonify({'code': '1','msg': '查询出来', 'data': data})

#价格走势 折线图
@detail_api.route('/brokenlinedata/<block>', methods=['post'])
def broken_line_data(block):
    # 获取房源发布时间戳数据
    # 从 House 模型中查询指定板块的房源发布时间，仅获取 publish_time 字段
    time_stamp = House.query.with_entities(House.publish_time).filter(House.block == block).all()
    # 按发布时间倒序排序，最新的时间在前
    time_stamp.sort(reverse=True)

    # 生成最近 14 天的日期列表（基于最新房源发布时间推算）
    date_list = []
    for i in range(1, 14):
        # 将查询到的时间戳（取第一条数据的时间戳，需确保有数据，否则可能报错）转换为 datetime 对象
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))  
        # 计算最新发布时间往前推 i 天的日期
        day = latest_release + timedelta(days=-i)  
        # 将日期格式化为 “月-日” 字符串，添加到日期列表
        date_list.append(day.strftime("%m-%d"))  
    # 反转日期列表，让日期按从早到晚排列（因为前面是倒着推算添加的）
    date_list.reverse()

    # 查询 1 室 1 厅户型的房价（房价/面积）趋势数据
    # 计算指定板块、1室1厅户型的 房价/面积 的平均值，按发布时间分组、排序
    rooms1 = House.query.with_entities(func.avg(House.price / House.area)) \
       .filter(
            House.block == block,  # 筛选板块
            House.rooms == '1室1厅'  # 筛选户型
        ) \
       .group_by(House.publish_time) \
       .order_by(House.publish_time) \
       .all()
    # 处理查询结果，取最近 14 条数据，保留 2 位小数，存入 data 列表
    data1 = []
    for i in rooms1[-14:]:
        data1.append(round(i[0], 2))

    # 2 室 1 厅户型的房价（房价/面积）趋势数据
    rooms2 = House.query.with_entities(func.avg(House.price / House.area)) \
       .filter(
            House.block == block,
            House.rooms == '2室1厅'
        ) \
       .group_by(House.publish_time) \
       .order_by(House.publish_time) \
       .all()
    data2 = []
    for i in rooms2[-14:]:
        data2.append(round(i[0], 2))

    # 2 室 2 厅户型的房价（房价/面积）趋势数据
    rooms3 = House.query.with_entities(func.avg(House.price / House.area)) \
       .filter(
            House.block == block,
            House.rooms == '2室2厅'
        ) \
       .group_by(House.publish_time) \
       .order_by(House.publish_time) \
       .all()
    data3= []
    for i in rooms3[-14:]:
        data3.append(round(i[0], 2))

    # 3 室 2 厅户型的房价（房价/面积）趋势数据
    rooms4 = House.query.with_entities(func.avg(House.price / House.area)) \
       .filter(
            House.block == block,
            House.rooms == '3室2厅'
        ) \
       .group_by(House.publish_time) \
       .order_by(House.publish_time) \
       .all()
    data4= []
    for i in rooms4[-14:]:
        data4.append(round(i[0], 2))

    return jsonify({'code': '1','msg': '查询出来', 'data': {
        '1室1厅':data1,
        '2室1厅':data2,
        '2室2厅':data3,
        '3室2厅':data4,
        'date_li':date_list

    }})

#线性回归点状图
@detail_api.route('/f_line_data/<block>', methods=['POST'])
def f_line_data(block):
    # 获取该block下所有房源的publish_time
    time_stamps = House.query.with_entities(House.publish_time).filter(House.block == block).all()
    if not time_stamps:
        return jsonify({'code': '0', 'msg': '无数据', 'data': {}})
    time_stamps = sorted([int(ts[0]) for ts in time_stamps], reverse=True)
    latest_time = datetime.fromtimestamp(time_stamps[0])

    date_li = []
    avg_price = []
    for i in range(14, 0, -1):
        day = latest_time - timedelta(days=i)
        day_start = int(datetime(day.year, day.month, day.day, 0, 0, 0).timestamp())
        day_end = int(datetime(day.year, day.month, day.day, 23, 59, 59).timestamp())
        # 查询当天所有房源的平均单价
        result = House.query.with_entities(func.avg(House.price / House.area))\
            .filter(House.block == block)\
            .filter(House.publish_time >= day_start, House.publish_time <= day_end)\
            .first()
        avg = round(result[0], 2) if result and result[0] else None
        date_li.append(day.strftime("%m-%d"))
        avg_price.append(avg if avg else None)

    return jsonify({'code': '1', 'msg': '查询成功', 'data': {'date_li': date_li, 'avg_price': avg_price}})