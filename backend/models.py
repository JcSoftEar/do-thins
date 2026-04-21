from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(128), unique=True, nullable=False, comment='微信OpenID')
    session_key = db.Column(db.String(128), nullable=True, comment='会话密钥')
    nickname = db.Column(db.String(64), nullable=True, comment='昵称')
    avatar_url = db.Column(db.String(256), nullable=True, comment='头像URL')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    lists = db.relationship('TodoList', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    checkins = db.relationship('CheckIn', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    shares = db.relationship('Share', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'nickname': self.nickname,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TodoList(db.Model):
    """清单表"""
    __tablename__ = 'todo_lists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    title = db.Column(db.String(128), nullable=False, comment='清单标题')
    items = db.Column(db.Text, nullable=False, comment='清单内容(JSON数组)')
    status = db.Column(db.Integer, default=0, comment='状态: 0-进行中, 1-已完成')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    checkins = db.relationship('CheckIn', backref='todo_list', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'items': json.loads(self.items) if self.items else [],
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CheckIn(db.Model):
    """打卡记录表"""
    __tablename__ = 'checkins'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False, comment='清单ID')
    checkin_date = db.Column(db.Date, nullable=False, comment='打卡日期')
    completed_items = db.Column(db.Text, nullable=True, comment='完成的项(JSON数组)')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'list_id', 'checkin_date', name='uq_user_list_date'),
    )
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'list_id': self.list_id,
            'checkin_date': self.checkin_date.isoformat() if self.checkin_date else None,
            'completed_items': json.loads(self.completed_items) if self.completed_items else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Share(db.Model):
    """分享记录表"""
    __tablename__ = 'shares'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False, comment='清单ID')
    share_code = db.Column(db.String(64), unique=True, nullable=False, comment='分享码')
    view_count = db.Column(db.Integer, default=0, comment='浏览次数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'list_id': self.list_id,
            'share_code': self.share_code,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
