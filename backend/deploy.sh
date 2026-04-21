#!/bin/bash
# 部署脚本 - 腾讯云

set -e

echo "===== 100件事清单后端部署 ====="

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt -q

# 初始化数据库
echo "初始化数据库..."
python init_db.py

# 使用gunicorn启动（生产环境）
echo "启动服务..."
gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon

echo "===== 部署完成 ====="
echo "服务地址: http://0.0.0.0:5000"
echo "API文档: http://0.0.0.0:5000/api/health"
