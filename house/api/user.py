from flask import Blueprint, request, jsonify, session, render_template
from models import db, User
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from models import House

# AES密钥和IV（生产环境建议用环境变量）
AES_KEY = b'1234567890abcdef'  # 16字节
AES_IV = b'abcdef1234567890'   # 16字节

user_api = Blueprint('user_api', __name__)

def encrypt_password(password):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    ct_bytes = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    ct_b64 = base64.b64encode(ct_bytes).decode('utf-8')
    return ct_b64

def decrypt_password(enc_password):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    ct_bytes = base64.b64decode(enc_password)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode('utf-8')

# 注册接口
@user_api.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')
    email = request.form.get('email')
    addr = request.form.get('addr')

    if not name or not password or not email:
        return jsonify({'valid': '0', 'msg': '用户名、密码、邮箱不能为空'})

    if User.query.filter_by(name=name).first():
        return jsonify({'valid': '0', 'msg': '用户名已存在'})

    enc_pwd = encrypt_password(password)
    user = User(name=name, password=enc_pwd, email=email, addr=addr)
    db.session.add(user)
    db.session.commit()
    # 注册成功后自动登录
    session['user_id'] = user.id
    session['name'] = user.name
    resp = jsonify({'valid': '1', 'msg': name})
    resp.set_cookie('name', user.name, max_age=300)  # 5分钟
    return resp

# 登录接口
@user_api.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name).first()
    if user:
        try:
            dec_pwd = decrypt_password(user.password)
            if dec_pwd == password:
                session['user_id'] = user.id
                session['name'] = user.name  # 存储用户名到session
                resp = jsonify({'valid': '1', 'msg': name})
                resp.set_cookie('name', user.name, max_age=300)  # 5分钟
                return resp
        except Exception:
            pass
    return jsonify({'valid': '0', 'msg': '用户名或密码错误'})

# 退出登录接口
@user_api.route('/logout', methods=['GET'])
def logout():
    # 清除session中的用户信息
    session.pop('user_id', None)
    session.pop('name', None)
    return jsonify({'valid': '1', 'msg': '退出成功'})

# 用户信息修改接口
@user_api.route('/user/update', methods=['POST'])
def update_user():
    old_name = session.get('name')  # 获取当前session中的用户名
    new_name = request.form.get('name')
    addr = request.form.get('addr')
    password = request.form.get('password')
    email = request.form.get('email')
    
    # 用session中的用户名唯一定位用户
    user = User.query.filter_by(name=old_name).first()
    if not user:
        return jsonify({'valid': '0', 'msg': '用户不存在'})
    
    # 昵称校验 - 昵称不能为空
    if not new_name or not new_name.strip():
        return jsonify({'valid': '0', 'msg': '昵称不能为空'})
    
    # 如果昵称发生变化，检查新昵称是否已存在
    if new_name != old_name:
        existing_user = User.query.filter_by(name=new_name).first()
        if existing_user:
            return jsonify({'valid': '0', 'msg': '昵称已存在'})
        # 更新昵称
        user.name = new_name
        # 更新session中的用户名
        session['name'] = new_name
    
    # 只有非空字段才更新数据库
    if addr and addr.strip():
        user.addr = addr.strip()
    if email and email.strip():
        user.email = email.strip()
    if password and password.strip():
        user.password = encrypt_password(password)
    
    db.session.commit()
    resp = jsonify({
        'valid': '1', 
        'msg': '信息已更新',
        'data': {
            'name': user.name
        }
    })
    resp.set_cookie('name', user.name, max_age=300)  # 5分钟
    return resp

#表单信息回显
@user_api.route('/user/info', methods=['GET'])
def user_info():
    name = session.get('name')
    if not name:
        return jsonify({'valid': '0', 'msg': '未登录'})
    user = User.query.filter_by(name=name).first()
    if not user:
        return jsonify({'valid': '0', 'msg': '用户不存在'})
    return jsonify({
        'valid': '1',
        'data': {
            'name': user.name,
            'addr': user.addr or '',
            'email': user.email or '',
            'password': '********'
        }
    })

# #收藏房源、浏览记录回显
# @user_api.route('/user/collect')
# def user_center():
#     if 'name' not in session:
#         # 未登录可重定向或返回空
#         return redirect('/')
#     user = User.query.get(session["user_id"])
#     #收藏房源
#     collect_houses = []
#     if user and user.collect_id:
#         id_list = [int(i) for i in user.collect_id.split('、') if i]
#         if id_list:
#             collect_houses = House.query.filter(House.id.in_(id_list)).all()
#             print(collect_houses)
#     #浏览记录
#     seen_houses = []
#     if user and user.seen_id:
#         seen_id_list = [int(i) for i in user.seen_id.split('、') if i]
#         if seen_id_list:
#             seen_houses = House.query.filter(House.id.in_(seen_id_list)).all()
#     return render_template('user.html', collect_houses=collect_houses, seen_houses=seen_houses)


#取消收藏
@user_api.route('/user/uncollect', methods=['POST'])
def user_uncollect():
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

