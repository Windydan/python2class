from flask import Flask, render_template

# 首页
from page.index import index_page
from page.detail import detail_page
from page.user import user_page
from page.list import list_page

# 用户API
from api.user import user_api

# 引入数据库配置
from config import Config
from models import db

app = Flask(__name__)

# 注册首页
app.register_blueprint(index_page, url_prefix='/')

# 详情页
app.register_blueprint(detail_page, url_prefix='/')

# 个人中心
app.register_blueprint(user_page, url_prefix='/')

# 列表
app.register_blueprint(list_page, url_prefix='/')

# 注册用户登录与注册接口
app.register_blueprint(user_api, url_prefix='/')

# 连接数据库
app.config.from_object(Config)
db.init_app(app)


# 注册用户相关API蓝图
#app.register_blueprint(user_api, url_prefix='/api/user')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 自动建表
    app.run(host='127.0.0.1', port=8000, debug=True)
