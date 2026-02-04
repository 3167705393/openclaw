#!/usr/bin/env python3
"""
综合性雪球内容获取解决方案
结合API搜索和备用方案来获取高质量内容
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional

class ComprehensiveXueqiuSolution:
    def __init__(self, u_value: str, xq_a_token: str, tavily_api_key: str):
        self.u_value = u_value
        self.xq_a_token = xq_a_token
        self.tavily_api_key = tavily_api_key
        
        # 初始化会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://xueqiu.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        # 设置登录凭证
        self.session.cookies.update({
            'u': self.u_value,
            'xq_a_token': self.xq_a_token
        })
    
    def try_direct_access(self) -> List[Dict]:
        """
        尝试直接访问雪球API
        """
        print("🔍 尝试直接访问雪球API...")
        
        try:
            # 先访问主页建立会话
            home_response = self.session.get('https://xueqiu.com/', timeout=10)
            
            if home_response.status_code == 200:
                print("✅ 成功访问主页")
            else:
                print(f"❌ 主页访问失败: {home_response.status_code}")
                return []
            
            # 尝试获取内容的多个API端点
            endpoints = [
                ('https://xueqiu.com/v4/statuses/public_timeline_by_category.json', {'category': '6', 'page': '1'}),
                ('https://xueqiu.com/statuses/hot_timeline.json', {'page': '1', 'size': '10'}),
                ('https://xueqiu.com/trends/statuses.json', {'since_id': '-1', 'max_id': '-1', 'count': '10'})
            ]
            
            for url, params in endpoints:
                try:
                    response = self.session.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        print(f"✅ 从 {url} 获取到数据")
                        try:
                            data = response.json()
                            
                            # 根据不同API返回格式提取帖子
                            posts = []
                            if 'statuses' in data:
                                posts = data['statuses']
                            elif 'list' in data:
                                posts = data['list']
                            elif isinstance(data, list):
                                posts = data
                            
                            if posts:
                                print(f"   - 解析到 {len(posts)} 个帖子")
                                return self._format_posts(posts[:5])  # 返回前5个
                            
                        except json.JSONDecodeError:
                            print(f"   - 响应不是JSON格式")
                    else:
                        print(f"   - {url} 返回状态码: {response.status_code}")
                except Exception as e:
                    print(f"   - 访问 {url} 时出错: {e}")
                    continue
            
            print("❌ 所有API端点都无法获取有效数据")
            return []
            
        except Exception as e:
            print(f"❌ 直接访问时出错: {e}")
            return []
    
    def search_via_tavily(self) -> List[Dict]:
        """
        通过Tavily API搜索雪球相关内容
        """
        print("🔍 通过Tavily API搜索雪球相关内容...")
        
        # 多个搜索查询来获取不同类型的内容
        queries = [
            '雪球网 热门帖子 今日讨论',
            '雪球 投资者热议话题 最新',
            '雪球社区 高热度 投资讨论',
            '雪球 今日热门 投资观点'
        ]
        
        all_results = []
        
        for query in queries:
            print(f"   - 搜索: {query}")
            
            url = 'https://api.tavily.com/search'
            data = {
                'api_key': self.tavily_api_key,
                'query': query,
                'search_depth': 'advanced',
                'include_answer': True,
                'include_sources': True,
                'max_results': 3
            }
            
            try:
                response = requests.post(url, json=data, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('answer'):
                        # 创建模拟帖子结构
                        post = {
                            'title': f"Tavily搜索: {query}",
                            'content': result['answer'],
                            'author': 'Tavily搜索结果',
                            'time': 'N/A',
                            'likes': 0,
                            'comments': 0,
                            'shares': 0,
                            'url': 'N/A',
                            'method': 'tavily_search'
                        }
                        all_results.append(post)
                    
                    # 添加来源
                    sources = result.get('sources', [])
                    for source in sources[:2]:  # 每个查询最多2个来源
                        post = {
                            'title': source.get('title', '无标题'),
                            'content': source.get('content', '无内容')[:500],
                            'author': 'Tavily来源',
                            'time': 'N/A',
                            'likes': 0,
                            'comments': 0,
                            'shares': 0,
                            'url': source.get('url', 'N/A'),
                            'method': 'tavily_source'
                        }
                        all_results.append(post)
                
                time.sleep(1)  # 避免请求过于频繁
                
            except Exception as e:
                print(f"   - Tavily搜索出错: {e}")
                continue
        
        print(f"✅ 通过Tavily获取到 {len(all_results)} 个结果")
        return all_results
    
    def _format_posts(self, raw_posts: List) -> List[Dict]:
        """
        格式化原始帖子数据
        """
        formatted_posts = []
        
        for post in raw_posts:
            if isinstance(post, dict):
                # 处理不同API返回的格式
                formatted = {
                    'title': post.get('title', post.get('description', '无标题')),
                    'content': post.get('text', post.get('description', '无内容')),
                    'author': post.get('user', {}).get('screen_name', '未知作者'),
                    'time': post.get('created_at', '未知时间'),
                    'likes': post.get('like_count', 0),
                    'comments': post.get('comment_count', 0),
                    'shares': post.get('retweet_count', 0),
                    'url': f"https://xueqiu.com{post.get('target', '')}",
                    'method': 'direct_api'
                }
                formatted_posts.append(formatted)
        
        return formatted_posts
    
    def get_comprehensive_content(self) -> List[Dict]:
        """
        获取综合内容：优先尝试直接访问，失败则使用Tavily搜索
        """
        print("🚀 开始获取雪球综合内容")
        print("="*60)
        
        # 首先尝试直接访问
        direct_posts = self.try_direct_access()
        
        if direct_posts:
            print(f"✅ 直接访问成功，获取到 {len(direct_posts)} 个帖子")
            return direct_posts
        else:
            print("⚠️ 直接访问失败，切换到Tavily搜索方案")
            tavily_posts = self.search_via_tavily()
            return tavily_posts

def main():
    # 从环境变量获取API密钥
    tavily_api_key = os.environ.get('TAVILY_API_KEY')
    if not tavily_api_key:
        print("❌ 未找到Tavily API密钥")
        return
    
    # 使用提供的登录凭证
    solution = ComprehensiveXueqiuSolution(
        u_value="8603655584",
        xq_a_token="17fa2787f256c2057245b461d0c6085a10db6eef",
        tavily_api_key=tavily_api_key
    )
    
    # 获取综合内容
    posts = solution.get_comprehensive_content()
    
    print("\\n" + "="*60)
    print("📊 最终获取到的内容:")
    print("="*60)
    
    if posts:
        for i, post in enumerate(posts, 1):
            print(f"\\n{i}. 📝 {post['title']}")
            print(f"   👤 作者: {post['author']}")
            print(f"   📅 时间: {post['time']}")
            print(f"   📄 内容: {post['content'][:300]}{'...' if len(post['content']) > 300 else ''}")
            print(f"   📊 互动: 👍{post['likes']} 💬{post['comments']} 🔄{post['shares']}")
            print(f"   🔗 链接: {post['url']}")
            print(f"   🛠️  方式: {post['method']}")
            print("-" * 50)
    else:
        print("❌ 未能获取到任何内容")
        print("\\n💡 建议:")
        print("   - 检查登录凭证是否正确")
        print("   - 尝试在不同时间段访问")
        print("   - 可能需要使用代理或VPN")
        print("   - 验证API密钥是否有效")

if __name__ == "__main__":
    main()