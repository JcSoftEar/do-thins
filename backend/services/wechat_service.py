import requests
from config import Config

class WeChatService:
    """微信服务"""
    
    @staticmethod
    def code2session(code: str) -> dict:
        """
        通过code获取session信息
        微信小程序的code2Session接口
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            'appid': Config.WECHAT_APPID,
            'secret': Config.WECHAT_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'errcode' in data and data['errcode'] != 0:
                return {
                    'success': False,
                    'error': data.get('errmsg', 'unknown error')
                }
            
            return {
                'success': True,
                'openid': data.get('openid'),
                'session_key': data.get('session_key'),
                'unionid': data.get('unionid')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_phone_number(phone_code: str) -> dict:
        """
        获取手机号
        phone_code: 手机号获取的code
        """
        # 此接口需要服务端向微信获取手机号
        # 具体实现根据微信官方文档
        return {
            'success': False,
            'error': 'Not implemented - requires phone number SDK'
        }
