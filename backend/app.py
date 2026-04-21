from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes.api import api
from routes.admin import admin

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
    app.register_blueprint(admin)
    
    # 提供管理后台页面
    @app.route('/admin/')
    def admin_page():
        import os
        admin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'admin')
        return send_from_directory(admin_path, 'index.html')
    
    @app.route('/admin/<path:filename>')
    def admin_static(filename):
        import os
        admin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'admin')
        return send_from_directory(admin_path, filename)
    
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
