from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    addr = db.Column(db.String(100))
    collect_id = db.Column(db.String(250))
    seen_id = db.Column(db.String(250))