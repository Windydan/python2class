from flask import Flask, Blueprint, render_template,request,jsonify
from models import House,db
from sqlalchemy import func

# 创建蓝图，蓝图名称为index_page
index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def index():
     # 获取房源总量
    house_total_num = House.query.count()
    # 获取最新房源6条
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(8).all()
    for house in house_new_list:
     print(house.id, house.img, house.publish_time)
    # 获取热门房源4条
    house_hot_list  = House.query.order_by(House.page_views.desc()).limit(4).all()
    return render_template('index.html', total = house_total_num, new_list = house_new_list, hot_list = house_hot_list)

# 查询关键词功能 给前端返回查询后的数据
@index_page.route('/search/keyword/', methods=['post'])
def search_kw():
    # 搜索的关键词
    kw = request.form['kw']
    # 获取用户选择的搜索选项
    info = request.form['info']

    if info == "地区搜索":
        # 获取查询结构   House.address.contains(kw筛选 address 包含关键词 kw 的记录（模糊匹配）。
        house_data = House.query.with_entities(House.address, func.count()).filter(House.address.contains(kw))

        # 对查询结果进行分组、排序，并获取数量最多的钱9条房源信息
        result = house_data.group_by('address').order_by(func.count().desc()).limit(9).all()
        
        # 查询结果
        if result:
            data = []
            for i in result:
                # 将查询的数据添加到data中
                data.append({'t_name': i[0], 'num': i[1]})
                return jsonify({'code': 1, 'msg': '查询成功', 'data': data})
        else:
            return jsonify({'code': 0, 'msg': '暂无数据', 'data': []})
        
    elif info == "户型搜索":

        house_data = House.query.with_entities(House.rooms, func.count()).filter(House.rooms.contains(kw))

        result = house_data.group_by('rooms').order_by(func.count().desc()).limit(9).all()

        if result:
            data = []
            for i in result:
                # 将查询的数据添加到data中
                data.append({'t_name': i[0], 'num': i[1]})
                return jsonify({'code': 1, 'msg': '查询成功', 'data': data})
        else:
            return jsonify({'code': 0, 'msg': '暂无数据', 'data': []})





