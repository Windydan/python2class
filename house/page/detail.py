from flask import Flask, Blueprint, render_template

detail_page = Blueprint('detail_page', __name__)

@detail_page.route('/house')
def index():
    return render_template('detail.html')
