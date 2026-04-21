#!/usr/bin/env python3
"""
数据库初始化脚本
运行此脚本创建数据库表（适用于 SQLite）
"""
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import User, TodoList, CheckIn, Share

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 删除旧数据库文件（如果存在）
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'do_things.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"已删除旧数据库: {db_path}")
        
        # 创建所有表
        db.create_all()
        print("所有数据库表已创建成功!")
        
        # 验证表是否创建
        tables = db.engine.table_names()
        print(f"已创建的表: {tables}")

if __name__ == '__main__':
    init_database()
