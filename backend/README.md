"""
100件事清单后端API

基于Python + SQLite的后端服务（开发环境）
生产环境建议使用 MySQL

API接口:
- POST /api/wechat/login          微信登录
- POST /api/ai/generate           AI生成100件事清单
- GET  /api/lists                 获取用户清单列表
- GET  /api/lists/<id>            获取清单详情
- POST /api/checkin               打卡
- GET  /api/checkin/history       获取打卡历史
- POST /api/share                 创建分享链接
- GET  /api/share/<code>          通过分享码获取清单
- GET  /api/health                健康检查

依赖:
- Flask==3.0.0
- Flask-CORS==4.0.0
- Flask-SQLAlchemy==3.1.1
- SQLAlchemy==2.0.23
- python-dotenv==1.0.0
- requests==2.31.0

安装:
pip install -r requirements.txt

配置:
cp .env.example .env
# 编辑 .env 填入配置

初始化数据库:
python init_db.py

启动服务:
python app.py

数据库说明:
- 默认使用 SQLite (do_things.db)，适合开发和快速部署
- 生产环境建议切换到 MySQL，修改 config.py 中的 SQLALCHEMY_DATABASE_URI
"""
