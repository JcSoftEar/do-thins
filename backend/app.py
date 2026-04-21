from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.api import api

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 初始化扩展
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(api)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
