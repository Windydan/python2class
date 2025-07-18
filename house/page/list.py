from flask import Flask, Blueprint, render_template

list_page = Blueprint('list_page', __name__)

@list_page.route('/list')
def index():
    return render_template('list.html')

