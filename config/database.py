# config/database.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'port': int(os.getenv('DB_PORT', 3306))
}

# AI 配置
AI_CONFIG = {
    'deepseek_api_key': os.getenv('DEEPSEEK_API_KEY'),
    'api_base': 'https://api.deepseek.com',
    'model': 'deepseek-chat',
    'temperature': 0.7,
    'max_tokens': 2000
}