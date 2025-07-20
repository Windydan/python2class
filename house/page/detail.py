from flask import Flask, Blueprint, render_template
from models import db,House

detail_page = Blueprint('detail_page', __name__)

@detail_page.route('/house/<int:house_id>')
def house_detail(house_id):
    house = House.query.get_or_404(house_id)
    print('访问的house_id:', house_id)
    house.page_views = (house.page_views or 0) + 1
    db.session.commit()
    return render_template('detail.html', house=house)
