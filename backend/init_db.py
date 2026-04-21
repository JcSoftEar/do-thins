#!/usr/bin/env python3
"""
数据库初始化脚本
运行此脚本创建数据库表
"""
import pymysql
from config import Config

def init_database():
    """初始化数据库"""
    # 连接MySQL服务器
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD
    )
    
    try:
        with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{Config.MYSQL_DATABASE}' created or already exists")
        
        connection.commit()
    finally:
        connection.close()
    
    print("Database initialization complete!")

if __name__ == '__main__':
    init_database()
