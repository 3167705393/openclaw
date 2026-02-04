#!/usr/bin/env python3
"""
增强版雪球帖子获取器
使用登录凭证获取完整的帖子内容
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime

class EnhancedXueqiuFetcher:
    def __init__(self, u_value: str, xq_a_token: str):
        """
        初始化雪球获取器
        :param u_value: 雪球用户ID (u cookie)
        :param xq_a_token: 雪球认证令牌 (xq_a_token cookie)
        """
        self.u_value = u_value
        self.xq_a_token = xq_a_token
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://xueqiu.com/',
            'Accept': 'application/json, text/html, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        
        # 设置登录凭证
        self.session.cookies.update({
            'u': self.u_value,
            'xq_a_token': self.xq_a_token
        })
    
    def get_hot_topics(self, count: int = 10) -> List[Dict]:
        """
        获取热门话题
        """
        try:
            url = "https://xueqiu.com/v2/statuses/mini.json"
            params = {
                'page': 1,
                'size': count,
                't': int(time.time() * 1000)  # 添加时间戳
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'statuses' in data:
                        return data['statuses']
                    else:
                        print(f"警告: 返回数据格式异常: {data}")
                        return []
                except json.JSONDecodeError:
                    print(f"警告: 响应不是JSON格式: {response.text[:200]}...")
                    return []
            else:
                print(f"获取热门话题失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text[:200]}...")
                return []
        except Exception as e:
            print(f"获取热门话题时出错: {e}")
            return []
    
    def search_posts(self, query: str, count: int = 10) -> List[Dict]:
        """
        搜索帖子
        """
        try:
            url = "https://xueqiu.com/statuses/search.json"
            params = {
                'q': query,
                'count': count,
                'page': 1,
                't': int(time.time() * 1000)  # 添加时间戳
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'statuses' in data:
                        return data['statuses']
                    else:
                        print(f"警告: 搜索返回数据格式异常: {data}")
                        return []
                except json.JSONDecodeError:
                    print(f"警告: 搜索响应不是JSON格式: {response.text[:200]}...")
                    return []
            else:
                print(f"搜索帖子失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text[:200]}...")
                return []
        except Exception as e:
            print(f"搜索帖子时出错: {e}")
            return []
    
    def get_post_detail(self, post_id: str) -> Dict:
        """
        获取单个帖子的详细内容
        """
        try:
            url = f"https://xueqiu.com/statuses/original/show.json"
            params = {
                'id': post_id,
                't': int(time.time() * 1000)
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    print(f"警告: 获取帖子详情响应不是JSON格式: {response.text[:200]}...")
                    return {}
            else:
                print(f"获取帖子详情失败，状态码: {response.status_code}")
                return {}
        except Exception as e:
            print(f"获取帖子详情时出错: {e}")
            return {}
    
    def format_post(self, post: Dict) -> str:
        """
        格式化帖子内容
        """
        user_info = post.get('user', {})
        formatted = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 帖子ID: {post.get('id', 'N/A')}
👤 作者: {user_info.get('screen_name', '匿名用户')} (@{user_info.get('id', 'N/A')})
📝 标题: {post.get('title', '无标题')}
📅 发布时间: {post.get('created_at', '未知时间')}
📈 互动数据: 👍 {post.get('like_count', 0)} | 💬 {post.get('comment_count', 0)} | 🔄 {post.get('retweet_count', 0)}
🔗 原文链接: https://xueqiu.com{post.get('target', '')}

📝 帖子内容:
{post.get('text', '无内容')}

🏷️ 标签: {', '.join([tag.get('tag', '') for tag in post.get('tags', [])]) if post.get('tags') else '无标签'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        return formatted.strip()

def main():
    print("🎯 增强版雪球帖子获取器")
    print("="*60)
    print("💡 请输入您的登录凭证来获取完整的帖子内容")
    
    # 由于这是演示，我们不会真正要求输入
    print("\n🔧 已准备好使用您之前提供的凭证:")
    print("   - 用户ID: 8603655584")
    print("   - 认证令牌: 17fa2787f256c2057245b461d0c6085a10db6eef")
    
    print("\n🔍 正在获取热门帖子...")
    
    # 创建获取器实例（使用您提供的凭证）
    fetcher = EnhancedXueqiuFetcher("8603655584", "17fa2787f256c2057245b461d0c6085a10db6eef")
    
    # 获取热门话题
    hot_posts = fetcher.get_hot_topics(count=5)
    
    if hot_posts:
        print(f"\n🎉 找到 {len(hot_posts)} 个热门帖子:")
        
        for i, post in enumerate(hot_posts, 1):
            print(f"\n{i}. {fetcher.format_post(post)}")
    else:
        print("\n❌ 未能获取到帖子内容")
        print("💡 可能的原因:")
        print("   - 登录凭证已过期")
        print("   - 网络请求被限制")
        print("   - API接口变更")
        print("\n📋 建议:")
        print("   - 检查并更新登录凭证")
        print("   - 稍后再试")
        print("   - 确保网络连接正常")

if __name__ == "__main__":
    main()