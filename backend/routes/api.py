import json
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, User, TodoList, CheckIn, Share
from services.wechat_service import WeChatService

api = Blueprint('api', __name__, url_prefix='/api')

def generate_share_code():
    """生成唯一的分享码"""
    return uuid.uuid4().hex[:12]

# ========== 微信登录 ==========

@api.route('/wechat/login', methods=['POST'])
def wechat_login():
    """微信登录接口"""
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({'success': False, 'error': 'code is required'}), 400
    
    # 调用微信服务获取openid
    result = WeChatService.code2session(code)
    
    if not result['success']:
        return jsonify({'success': False, 'error': result['error']}), 400
    
    openid = result['openid']
    session_key = result.get('session_key')
    
    # 查询或创建用户
    user = User.query.filter_by(openid=openid).first()
    if not user:
        user = User(
            openid=openid,
            session_key=session_key,
            nickname=data.get('nickname', ''),
            avatar_url=data.get('avatar_url', '')
        )
        db.session.add(user)
        db.session.commit()
    else:
        # 更新session_key
        user.session_key = session_key
        db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict(),
            'token': f"jwt_{openid}"  # 简化版token，实际项目应用JWT
        }
    })

# ========== AI生成清单 ==========

@api.route('/ai/generate', methods=['POST'])
def generate_list():
    """AI生成100件事清单"""
    data = request.get_json()
    user_id = data.get('user_id')
    prompt = data.get('prompt')
    title = data.get('title', '我的100件事')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id is required'}), 400
    
    # 验证用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # 调用MiniMax生成清单
    from services.minimax_service import MiniMaxService
    things = MiniMaxService.generate_100_things(prompt)
    
    # 创建清单记录
    todo_list = TodoList(
        user_id=user_id,
        title=title,
        items=json.dumps(things, ensure_ascii=False),
        status=0
    )
    db.session.add(todo_list)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': todo_list.to_dict()
    })

# ========== 获取清单 ==========

@api.route('/lists', methods=['GET'])
def get_lists():
    """获取用户的所有清单"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id is required'}), 400
    
    lists = TodoList.query.filter_by(user_id=user_id).order_by(TodoList.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in lists]
    })

@api.route('/lists/<int:list_id>', methods=['GET'])
def get_list(list_id):
    """获取单个清单详情"""
    todo_list = TodoList.query.get(list_id)
    
    if not todo_list:
        return jsonify({'success': False, 'error': 'List not found'}), 404
    
    return jsonify({
        'success': True,
        'data': todo_list.to_dict()
    })

# ========== 打卡 ==========

@api.route('/checkin', methods=['POST'])
def checkin():
    """打卡接口"""
    data = request.get_json()
    user_id = data.get('user_id')
    list_id = data.get('list_id')
    completed_items = data.get('completed_items', [])
    checkin_date = data.get('checkin_date', datetime.now().date().isoformat())
    
    if not user_id or not list_id:
        return jsonify({'success': False, 'error': 'user_id and list_id are required'}), 400
    
    # 检查清单是否存在
    todo_list = TodoList.query.get(list_id)
    if not todo_list:
        return jsonify({'success': False, 'error': 'List not found'}), 404
    
    # 检查当天是否已打卡
    existing = CheckIn.query.filter_by(
        user_id=user_id,
        list_id=list_id,
        checkin_date=checkin_date
    ).first()
    
    if existing:
        # 更新打卡记录
        existing.completed_items = json.dumps(completed_items, ensure_ascii=False)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': existing.to_dict(),
            'message': 'Check-in updated'
        })
    
    # 创建新打卡记录
    checkin_record = CheckIn(
        user_id=user_id,
        list_id=list_id,
        checkin_date=checkin_date,
        completed_items=json.dumps(completed_items, ensure_ascii=False)
    )
    db.session.add(checkin_record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': checkin_record.to_dict(),
        'message': 'Check-in successful'
    })

@api.route('/checkin/history', methods=['GET'])
def checkin_history():
    """获取打卡历史"""
    user_id = request.args.get('user_id')
    list_id = request.args.get('list_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id is required'}), 400
    
    query = CheckIn.query.filter_by(user_id=user_id)
    if list_id:
        query = query.filter_by(list_id=list_id)
    
    records = query.order_by(CheckIn.checkin_date.desc()).limit(30).all()
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in records]
    })

# ========== 分享 ==========

@api.route('/share', methods=['POST'])
def create_share():
    """创建分享链接"""
    data = request.get_json()
    user_id = data.get('user_id')
    list_id = data.get('list_id')
    
    if not user_id or not list_id:
        return jsonify({'success': False, 'error': 'user_id and list_id are required'}), 400
    
    # 检查清单是否存在
    todo_list = TodoList.query.get(list_id)
    if not todo_list:
        return jsonify({'success': False, 'error': 'List not found'}), 404
    
    # 检查是否已有分享码
    existing = Share.query.filter_by(user_id=user_id, list_id=list_id).first()
    if existing:
        return jsonify({
            'success': True,
            'data': existing.to_dict()
        })
    
    # 创建分享记录
    share = Share(
        user_id=user_id,
        list_id=list_id,
        share_code=generate_share_code()
    )
    db.session.add(share)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': share.to_dict()
    })

@api.route('/share/<share_code>', methods=['GET'])
def get_shared_list(share_code):
    """通过分享码获取清单"""
    share = Share.query.filter_by(share_code=share_code).first()
    
    if not share:
        return jsonify({'success': False, 'error': 'Share not found'}), 404
    
    # 增加浏览次数
    share.view_count += 1
    db.session.commit()
    
    todo_list = TodoList.query.get(share.list_id)
    
    return jsonify({
        'success': True,
        'data': {
            'share': share.to_dict(),
            'list': todo_list.to_dict() if todo_list else None,
            'user': todo_list.user.to_dict() if todo_list else None
        }
    })

# ========== 健康检查 ==========

@api.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'success': True,
        'message': 'Service is running',
        'timestamp': datetime.now().isoformat()
    })
