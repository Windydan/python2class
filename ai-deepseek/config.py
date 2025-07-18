from dotenv import load_dotenv
import os

# 将 .env 文件中的环境变量加载到系统中
load_dotenv()

class Config:
    # 访问环境变量
    DEEPSEEK_API_KEY= os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    KIMI_API_KEY= os.getenv('KIMI_API_KEY')
    KIMI_BASE_URL = os.getenv('KIMI_BASE_URL')
