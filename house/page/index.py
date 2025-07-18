from flask import Flask, Blueprint, render_template

# 创建蓝图，蓝图名称为index_page
index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def index():
    return render_template('index.html')





