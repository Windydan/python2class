# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Windydan:mysql%40123@localhost:3306/house"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"  # 用于Flask session等
