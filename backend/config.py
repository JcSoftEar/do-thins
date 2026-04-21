import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'todo_100things')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MiniMax API Configuration
    MINIMAX_API_KEY = os.getenv('MINIMAX_API_KEY', '')
    MINIMAX_API_URL = os.getenv('MINIMAX_API_URL', 'https://api.minimax.chat/v1/text/chatcompletion_pro')
    MINIMAX_GROUP_ID = os.getenv('MINIMAX_GROUP_ID', '')
    
    # WeChat Configuration
    WECHAT_APPID = os.getenv('WECHAT_APPID', '')
    WECHAT_SECRET = os.getenv('WECHAT_SECRET', '')
    
    # JWT Secret
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
