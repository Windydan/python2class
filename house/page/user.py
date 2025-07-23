from flask import Flask, Blueprint, render_template, session, redirect

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
    
    return render_template('user.html', username=username)
