from flask import Flask, Blueprint, render_template, session, redirect,request, jsonify
from models import House,User,db
user_page = Blueprint('user_page', __name__)

@user_page.route('/user')
@user_page.route('/user/<username>')
def user_profile(username=None):
    # 如果没有登录，重定向到首页
    if not session.get('name'):
        return redirect('/')
    
    # 如果没有指定用户名，使用当前登录用户的用户名
    if username is None:
        username = session.get('name')

    user = User.query.filter_by(name=username).first()
    #收藏房源
    collect_houses = []
    if user and user.collect_id:
        id_list = [int(i) for i in user.collect_id.split('、') if i]
        if id_list:
            collect_houses = House.query.filter(House.id.in_(id_list)).all()
            print(collect_houses)
    #浏览记录
    seen_houses = []
    if user and user.seen_id:
        seen_id_list = [int(i) for i in user.seen_id.split('、') if i]
        if seen_id_list:
            seen_houses = House.query.filter(House.id.in_(seen_id_list)).all()
    return render_template('user.html', username=username,collect_houses=collect_houses, seen_houses=seen_houses)

# #取消收藏
# @user_page.route('/user/uncollect', methods=['POST'])
# def user_uncollect():
#     if 'name' not in session:
#         return jsonify({'valid': 0, 'msg': '未登录'})
#     user = User.query.filter_by(name=session['name']).first()
#     house_id = request.form.get('house_id')
#     if not user or not house_id:
#         return jsonify({'valid': 0, 'msg': '参数错误'})
#     collect_list = user.collect_id.split('、') if user.collect_id else []
#     if house_id in collect_list:
#         collect_list.remove(house_id)
#         user.collect_id = '、'.join([i for i in collect_list if i])
#         db.session.commit()
#     return jsonify({'valid': 1, 'msg': '已取消收藏'})