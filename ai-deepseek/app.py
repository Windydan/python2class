from flask import Flask, render_template, request, jsonify, Response, session, make_response
import os
from config import Config 
import secrets
import requests

# app = Flask("程序名称", static_folder="静态文件目录", template_folder="模板文件目录")
app = Flask(__name__, template_folder='templates')

# 生成一个强随机的 secret_key
secret_key = secrets.token_hex(32)  # 生成 64 字符的十六进制密钥（32字节）

# 会话key
app.secret_key = os.getenv('FLASK_SECRET_KEY') if os.getenv('FLASK_SECRET_KEY') else secret_key

# 支持的模型列表
AVAILABLE_MODELS = [
    {"id": "deepseek-chat", "name": "DeepSeek Chat"},
    {"id": "openai-gpt-3.5", "name": "OpenAI GPT-3.5"},
    {"id": "kimi-chat", "name": "Kimi Chat"}
]

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify({"models": AVAILABLE_MODELS})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    model = data.get('model', 'deepseek-chat')
    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400
    # 根据模型调用不同API
    if model == 'deepseek-chat':
        reply = call_deepseek_api(user_message)
    elif model == 'openai-gpt-3.5':
        reply = call_openai_api(user_message)
    elif model == 'kimi-chat':
        reply = call_kimi_api(user_message)
    else:
        reply = "暂不支持该模型"
    return jsonify({"reply": reply})

def call_deepseek_api(message):
    api_key = Config.DEEPSEEK_API_KEY
    print(f"DEEPSEEK_API_KEY: {api_key}")  # 打印出来检查
    base_url = Config.DEEPSEEK_BASE_URL or "https://api.deepseek.com"
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"[DeepSeek API错误]: {str(e)}"

def call_openai_api(message):
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[OpenAI API错误]: {str(e)}"

def call_kimi_api(message):
    api_key = Config.KIMI_API_KEY
    base_url = getattr(Config, "KIMI_BASE_URL", "https://api.moonshot.cn")
    url = f"{base_url}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "moonshot-v1-8k",  
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"[Kimi API错误]: {str(e)}"

@app.route('/')
def index():

    # 设置session
    if 'name' not in session:
        session['name'] = "root"

    resp = make_response(render_template('index.html'))
    # 设置cookie
    # resp.set_cookie('username', 'admin')

    # 删除cookie，设置过期时间，值为空，
    # resp.set_cookie('username', '', expires=0)

    # 获取cookie
    print(request.cookies.get('username'))

    # 删除session
    # session.pop('name', None)

    # 获取session
    print(session.get('name'))

    
    return resp

    # return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/subject/index')
def subjectindex():
    return render_template('subject/index.html')






if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
