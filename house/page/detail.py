from flask import Flask, Blueprint, render_template, redirect, session, request, jsonify
from models import db, House, User

detail_page = Blueprint('detail_page', __name__)

@detail_page.route('/house/<int:house_id>')
def house_detail(house_id):
    house = House.query.get_or_404(house_id)
    print('访问的house_id:', house_id)

    # 判断用户是否登录及是否已收藏
    is_collected = False
    user = None
    if 'name' in session:
        user = User.query.filter_by(name=session['name']).first()

        #获取收藏id
        if user and user.collect_id:
            collect_list = user.collect_id.split('、') if user.collect_id else []
            is_collected = str(house_id) in collect_list
        #获取浏览记录id
        if user:
            seen_list = user.seen_id.split('、') if user.seen_id else []
            if str(house_id) not in seen_list:
                seen_list.append(str(house_id))
                user.seen_id = '、'.join(seen_list)
                db.session.commit()

    if house:
        #增加房源浏览量
        house.page_views = (house.page_views or 0) + 1
        db.session.commit()
         # 获取房源对象的配套设施信息
        facilities = house.facilities
        # 将配套设施以-作为分割保存在列表facilities_list中
        facilities_list = facilities.split('-')
        # 定义一个用来存放推荐房源的列表变量
        recommend_list = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).limit(6).all()

        return render_template('detail.html', house=house, facilities=facilities_list, recommend = recommend_list, is_collected=is_collected, user=user)
    else:
        return redirect('/')

# 收藏房源接口
@detail_page.route('/house/collect', methods=['POST'])
def collect_house():
    if 'name' not in session:
        return jsonify({'valid': 0, 'msg': '未登录'})
    user = User.query.filter_by(name=session['name']).first()
    house_id = request.form.get('house_id')
    if not user or not house_id:
        return jsonify({'valid': 0, 'msg': '参数错误'})
    collect_list = user.collect_id.split('、') if user.collect_id else []
    if house_id not in collect_list:
        collect_list.append(house_id)
        user.collect_id = '、'.join([i for i in collect_list if i])
        db.session.commit()
    return jsonify({'valid': 1, 'msg': '已收藏'})

# 取消收藏接口
@detail_page.route('/house/uncollect', methods=['POST'])
def uncollect_house():
    if 'name' not in session:
        return jsonify({'valid': 0, 'msg': '未登录'})
    user = User.query.filter_by(name=session['name']).first()
    house_id = request.form.get('house_id')
    if not user or not house_id:
        return jsonify({'valid': 0, 'msg': '参数错误'})
    collect_list = user.collect_id.split('、') if user.collect_id else []
    if house_id in collect_list:
        collect_list.remove(house_id)
        user.collect_id = '、'.join([i for i in collect_list if i])
        db.session.commit()
    return jsonify({'valid': 1, 'msg': '已取消收藏'})

# 处理交通有无的情况
def deal_none(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word
    

detail_page.add_app_template_filter(deal_none, 'dealNone')
   

