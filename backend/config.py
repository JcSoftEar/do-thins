import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQLite Configuration (适合开发环境，生产环境建议使用 MySQL)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'do_things.db')
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
