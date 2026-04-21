#!/usr/bin/env python3
"""
API测试脚本
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """测试健康检查"""
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Health: {resp.json()}")

def test_generate():
    """测试AI生成清单"""
    resp = requests.post(f"{BASE_URL}/ai/generate", json={
        "user_id": 1,
        "title": "我的100件事",
        "prompt": "生成一个关于旅行的100件事清单"
    })
    print(f"Generate: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.json().get('data', {}).get('id')

def test_lists(user_id=1):
    """测试获取清单"""
    resp = requests.get(f"{BASE_URL}/lists?user_id={user_id}")
    print(f"Lists: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")

def test_checkin(list_id):
    """测试打卡"""
    resp = requests.post(f"{BASE_URL}/checkin", json={
        "user_id": 1,
        "list_id": list_id,
        "completed_items": ["学会游泳", "学习摄影"],
        "checkin_date": "2026-04-21"
    })
    print(f"Check-in: {resp.json()}")

def test_share(user_id=1, list_id=1):
    """测试分享"""
    resp = requests.post(f"{BASE_URL}/share", json={
        "user_id": user_id,
        "list_id": list_id
    })
    print(f"Share: {resp.json()}")
    return resp.json().get('data', {}).get('share_code')

def test_shared_list(share_code):
    """测试通过分享码获取"""
    resp = requests.get(f"{BASE_URL}/share/{share_code}")
    print(f"Shared List: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")

if __name__ == '__main__':
    print("===== API测试 =====")
    
    # 健康检查
    test_health()
    
    # 生成清单
    list_id = test_generate()
    
    # 获取清单
    test_lists()
    
    # 打卡
    if list_id:
        test_checkin(list_id)
    
    # 分享
    share_code = test_share(1, 1)
    
    # 获取分享
    if share_code:
        test_shared_list(share_code)
    
    print("===== 测试完成 =====")
