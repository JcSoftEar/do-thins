import requests
from config import Config

class MiniMaxService:
    """MiniMax大模型服务"""
    
    @staticmethod
    def generate_100_things(prompt: str = None) -> list:
        """
        调用MiniMax API生成100件事
        prompt: 可选的自定义提示词
        """
        if not Config.MINIMAX_API_KEY:
            # 如果没有配置API Key，返回示例数据
            return MiniMaxService._get_sample_list()
        
        default_prompt = """请生成一个包含100项事情的清单，主题是关于个人成长、自我提升或有趣的生活体验。
请以JSON数组格式返回，每项是一个字符串。
只返回JSON数组，不要包含其他文字。
格式示例：["事情1", "事情2", "事情3", ...]"""
        
        user_prompt = prompt or default_prompt
        
        headers = {
            'Authorization': f'Bearer {Config.MINIMAX_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'MiniMax-Text-01',
            'messages': [
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 4000
        }
        
        try:
            response = requests.post(
                Config.MINIMAX_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # 尝试解析JSON
            import json
            # 清理可能存在的markdown代码块
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            things = json.loads(content.strip())
            return things[:100]  # 确保最多100项
            
        except Exception as e:
            print(f"MiniMax API error: {e}")
            return MiniMaxService._get_sample_list()
    
    @staticmethod
    def _get_sample_list() -> list:
        """返回示例清单数据"""
        return [
            "学会一门编程语言", "每天阅读30分钟", "练习冥想10分钟", "学习游泳",
            "尝试100种不同的美食", "每周运动3次", "学习摄影技巧", "培养一个爱好",
            "写一篇博客文章", "学习一门外语", "完成一个马拉松", "学会烘焙面包",
            "阅读100本经典书籍", "学习绘画基础", "掌握时间管理技巧", "建立早起习惯",
            "学习投资理财知识", "参加志愿者活动", "完成一次徒步旅行", "学习茶道",
            "掌握公开演讲技巧", "学习写作技巧", "尝试极限运动", "建立人脉网络",
            "学习心理学基础", "掌握谈判技巧", "尝试新餐厅", "学习音乐理论",
            "练习瑜伽", "学习园艺", "掌握急救技能", "尝试单板滑雪",
            "学习网页开发", "阅读科幻小说", "尝试攀岩", "学习品酒",
            "练习书法", "学习舞蹈", "尝试帆船运动", "学习急救知识",
            "掌握压力管理", "学习哲学基础", "尝试潜水", "学习天文知识",
            "练习正念冥想", "学习历史知识", "尝试滑翔伞", "学习茶艺",
            "掌握情绪管理", "学习逻辑思维", "尝试马术", "学习建筑知识",
            "练习腹式呼吸", "学习政治常识", "尝试热气球", "学习文学鉴赏",
            "掌握自律习惯", "学习科学实验", "尝试滑雪", "学习戏曲欣赏",
            "练习感恩日记", "学习经济学基础", "尝试狩猎", "学习艺术史",
            "掌握积极倾听", "学习社会学基础", "尝试风筝冲浪", "学习音乐史",
            "练习自我反省", "学习伦理学", "尝试滑冰", "学习电影赏析",
            "掌握目标设定", "学习物理学基础", "尝试冲浪", "学习戏剧表演",
            "练习放松技巧", "学习化学基础", "尝试轮滑", "学习雕塑艺术",
            "掌握批判性思维", "学习生物学基础", "尝试跆拳道", "学习室内设计",
            "练习专注力训练", "学习地理知识", "尝试羽毛球", "学习服装搭配",
            "掌握记忆技巧", "学习数学基础", "尝试网球", "学习珠宝鉴赏",
            "练习沟通技巧", "学习统计学基础", "尝试高尔夫球", "学习陶艺",
            "掌握决策能力", "学习环境科学", "尝试保龄球", "学习插花艺术",
            "练习创造力培养", "学习市场营销", "尝试乒乓球", "学习扎染艺术",
            "掌握问题解决技巧", "学习项目管理", "尝试篮球", "学习数字绘画",
            "练习领导力培养", "学习团队协作", "尝试排球", "学习金属工艺"
        ]
