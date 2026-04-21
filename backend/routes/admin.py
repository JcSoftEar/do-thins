import uuid
import hashlib
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

admin = Blueprint('admin', __name__, url_prefix='/api/admin')

# ========== 管理员配置（简单方案：写死在代码中）==========
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # 实际项目中应加密存储

# 简单的Token存储（生产环境应使用Redis）
admin_tokens = {}

def generate_token():
    """生成简单的管理员Token"""
    return uuid.uuid4().hex

def verify_token(token):
    """验证Token是否有效"""
    if token in admin_tokens:
        if admin_tokens[token]['expires'] > datetime.now():
            return True
        else:
            # 删除过期Token
            del admin_tokens[token]
    return False

def require_admin(func):
    """管理员权限装饰器"""
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token or not verify_token(token):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ========== 管理员登录 ==========

@admin.route('/login', methods=['POST'])
def login():
    """管理员登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password are required'}), 400
    
    # 简单验证（实际项目中应从数据库验证）
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        token = generate_token()
        admin_tokens[token] = {
            'expires': datetime.now() + timedelta(days=7),
            'username': username
        }
        return jsonify({
            'success': True,
            'data': {
                'token': token,
                'username': username
            }
        })
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

# ========== 统计数据 ==========

@admin.route('/stats', methods=['GET'])
@require_admin
def get_stats():
    """获取统计数据"""
    from models import db, User, TodoList, CheckIn
    
    user_count = User.query.count()
    list_count = TodoList.query.count()
    checkin_count = CheckIn.query.count()
    
    return jsonify({
        'success': True,
        'data': {
            'user_count': user_count,
            'list_count': list_count,
            'checkin_count': checkin_count
        }
    })

# ========== 用户列表 ==========

@admin.route('/users', methods=['GET'])
@require_admin
def get_users():
    """获取用户列表"""
    from models import db, User, CheckIn
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    offset = (page - 1) * page_size
    
    # 获取用户列表
    users = User.query.order_by(User.created_at.desc()).offset(offset).limit(page_size).all()
    total = User.query.count()
    
    # 构建用户数据，包含打卡数
    user_list = []
    for user in users:
        checkin_count = CheckIn.query.filter_by(user_id=user.id).count()
        user_list.append({
            'id': user.id,
            'nickname': user.nickname or '未设置昵称',
            'avatar_url': user.avatar_url or '',
            'checkin_count': checkin_count,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    
    return jsonify({
        'success': True,
        'data': {
            'users': user_list,
            'total': total,
            'page': page,
            'page_size': page_size
        }
    })

# ========== 打卡记录列表 ==========

@admin.route('/checkins', methods=['GET'])
@require_admin
def get_checkins():
    """获取打卡记录列表"""
    from models import db, CheckIn, User, TodoList
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    offset = (page - 1) * page_size
    
    # 获取打卡记录
    checkins = CheckIn.query.order_by(CheckIn.created_at.desc()).offset(offset).limit(page_size).all()
    total = CheckIn.query.count()
    
    # 构建打卡记录数据
    checkin_list = []
    for checkin in checkins:
        user = User.query.get(checkin.user_id)
        todo_list = TodoList.query.get(checkin.list_id)
        
        import json
        completed_items = json.loads(checkin.completed_items) if checkin.completed_items else []
        
        checkin_list.append({
            'id': checkin.id,
            'user_id': checkin.user_id,
            'user_nickname': user.nickname if user else '未知用户',
            'list_id': checkin.list_id,
            'list_title': todo_list.title if todo_list else '未知清单',
            'checkin_date': checkin.checkin_date.isoformat() if checkin.checkin_date else None,
            'completed_items': completed_items,
            'completed_count': len(completed_items),
            'created_at': checkin.created_at.isoformat() if checkin.created_at else None
        })
    
    return jsonify({
        'success': True,
        'data': {
            'checkins': checkin_list,
            'total': total,
            'page': page,
            'page_size': page_size
        }
    })
