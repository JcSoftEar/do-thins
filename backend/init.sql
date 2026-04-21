-- 100件事清单数据库初始化SQL
-- 用于手动初始化数据库

CREATE DATABASE IF NOT EXISTS todo_100things CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE todo_100things;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    openid VARCHAR(128) UNIQUE NOT NULL COMMENT '微信OpenID',
    session_key VARCHAR(128) COMMENT '会话密钥',
    nickname VARCHAR(64) COMMENT '昵称',
    avatar_url VARCHAR(256) COMMENT '头像URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_openid (openid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 清单表
CREATE TABLE IF NOT EXISTS todo_lists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL COMMENT '用户ID',
    title VARCHAR(128) NOT NULL COMMENT '清单标题',
    items TEXT NOT NULL COMMENT '清单内容(JSON数组)',
    status INT DEFAULT 0 COMMENT '状态: 0-进行中, 1-已完成',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='清单表';

-- 打卡记录表
CREATE TABLE IF NOT EXISTS checkins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL COMMENT '用户ID',
    list_id INT NOT NULL COMMENT '清单ID',
    checkin_date DATE NOT NULL COMMENT '打卡日期',
    completed_items TEXT COMMENT '完成的项(JSON数组)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (list_id) REFERENCES todo_lists(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_list_date (user_id, list_id, checkin_date),
    INDEX idx_user_id (user_id),
    INDEX idx_list_id (list_id),
    INDEX idx_checkin_date (checkin_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='打卡记录表';

-- 分享记录表
CREATE TABLE IF NOT EXISTS shares (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL COMMENT '用户ID',
    list_id INT NOT NULL COMMENT '清单ID',
    share_code VARCHAR(64) UNIQUE NOT NULL COMMENT '分享码',
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (list_id) REFERENCES todo_lists(id) ON DELETE CASCADE,
    INDEX idx_share_code (share_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分享记录表';
