from flask import Flask, Blueprint, render_template,request,jsonify
from models import House

query_page = Blueprint('query_page', __name__)

@query_page.route('/query')
def search_txt_info():
    #获取地区字段的查询
    if request.args.get('addr'):
        addr = request.args.get('addr')
        result = House.query.filter(House.address == addr).order_by(House.publish_time.desc()).all()
        print(request.args.get('addr'))
        return render_template('list.html',house_list=result)
    #获取户型字段的查询
    if request.args.get('rooms'):
        rooms = request.args.get('rooms')
        result = House.query.filter(House.rooms == rooms).order_by(House.publish_time.desc()).all()
        print(request.args.get('rooms'))
        return render_template('list.html',house_list=result)
    #默认渲染首页
    return render_template('index_page.index')

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