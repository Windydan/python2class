from flask import Blueprint, request, jsonify, session
from models import db, User
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

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
    return jsonify({'valid': '1', 'msg': name})

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
                return jsonify({'valid': '1', 'msg': name})
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