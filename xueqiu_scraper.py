#!/usr/bin/env python3
"""
雪球帖子爬取器
用于获取完整的帖子内容
"""

import requests
import json
import time
from typing import Dict, List, Optional
from urllib.parse import urlencode

class XueqiuScraper:
    def __init__(self, cookies: Optional[Dict] = None):
        """
        初始化雪球爬取器
        :param cookies: 登录后的cookies，用于访问需要登录的内容
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://xueqiu.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        })
        
        if cookies:
            self.session.cookies.update(cookies)
    
    def search_topics(self, query: str, count: int = 10) -> List[Dict]:
        """
        搜索话题
        """
        search_url = "https://xueqiu.com/statuses/search.json"
        params = {
            'q': query,
            'count': count,
            'page': 1
        }
        
        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 提取帖子信息
            statuses = data.get('statuses', [])
            posts = []
            
            for status in statuses:
                post = {
                    'id': status.get('id'),
                    'user': status.get('user', {}).get('screen_name'),
                    'title': status.get('title', ''),
                    'description': status.get('description', ''),
                    'text': status.get('text', ''),
                    'created_at': status.get('created_at'),
                    'like_count': status.get('like_count', 0),
                    'comment_count': status.get('comment_count', 0),
                    'retweet_count': status.get('retweet_count', 0),
                    'href': f"https://xueqiu.com{status.get('target', '')}"
                }
                posts.append(post)
            
            return posts
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def get_post_detail(self, post_id: str) -> Dict:
        """
        获取单个帖子的详细内容
        """
        detail_url = f"https://xueqiu.com/statuses/original/show.json"
        params = {'id': post_id}
        
        try:
            response = self.session.get(detail_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取帖子详情失败: {e}")
            return {}
    
    def get_user_posts(self, user_id: str, count: int = 20) -> List[Dict]:
        """
        获取特定用户的帖子
        """
        user_url = f"https://xueqiu.com/v4/statuses/user_timeline.json"
        params = {
            'user_id': user_id,
            'page': 1,
            'count': count
        }
        
        try:
            response = self.session.get(user_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            statuses = data.get('statuses', [])
            posts = []
            
            for status in statuses:
                post = {
                    'id': status.get('id'),
                    'user': status.get('user', {}).get('screen_name'),
                    'title': status.get('title', ''),
                    'text': status.get('text', ''),
                    'created_at': status.get('created_at'),
                    'like_count': status.get('like_count', 0),
                    'comment_count': status.get('comment_count', 0),
                    'retweet_count': status.get('retweet_count', 0),
                    'href': f"https://xueqiu.com{status.get('target', '')}"
                }
                posts.append(post)
            
            return posts
        except Exception as e:
            print(f"获取用户帖子失败: {e}")
            return []

def demo_xueqiu_scraper():
    """
    演示雪球爬取器功能
    """
    print("🎯 雪球帖子爬取器演示")
    print("="*60)
    print("⚠️  注意：要获取完整帖子内容，需要登录凭证（cookies）")
    print("💡  请提供雪球登录后的cookies，以获取需要登录才能查看的内容")
    print("="*60)
    
    # 模拟展示功能，不实际访问
    print("\n📋 可用功能：")
    print("  1. search_topics(query) - 搜索话题")
    print("  2. get_post_detail(post_id) - 获取帖子详情") 
    print("  3. get_user_posts(user_id) - 获取用户帖子")
    
    print("\n🔐 使用方法：")
    print("  scraper = XueqiuScraper(cookies={'xueqiu_auth_token': 'your_token'})")
    print("  posts = scraper.search_topics('热门话题')")
    
    print("\n💡 如果您提供登录凭证，我可以获取完整的帖子内容。")

if __name__ == "__main__":
    demo_xueqiu_scraper()