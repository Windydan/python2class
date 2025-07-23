from flask import Flask, Blueprint, render_template, request, jsonify
from models import House
import math

query_page = Blueprint('query_page', __name__)

@query_page.route('/query', defaults={'page': 1})
@query_page.route('/query/<int:page>')
def search_txt_info(page):
    per_page = 10
    # 获取查询参数
    addr = request.args.get('addr')
    rooms = request.args.get('rooms')
    query = House.query
    if addr:
        query = query.filter(House.address == addr)
    if rooms:
        query = query.filter(House.rooms == rooms)
    # 总数和分页
    house_num = query.count()
    total_num = math.ceil(house_num / per_page)
    result = query.order_by(House.publish_time.desc()).paginate(page=page, per_page=per_page)
    return render_template('search.html', house_list=result.items, page_num=result.page, total_num=total_num, addr=addr, rooms=rooms)

#当房源标题长度大于15时用省略号
def deal_title_cover(title):
    if len(title)>15:
        return title[:15] + '...'
    else:
        return title
    
#房源朝向、交通条件为空，显示暂无信息
def deal_direction(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word
    
#添加过滤器
query_page.add_app_template_filter(deal_title_cover,'dealover')
query_page.add_app_template_filter(deal_direction,'dealdirection')