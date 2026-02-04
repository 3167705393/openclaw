#!/usr/bin/env python3
"""
雪球浏览器自动化获取器
使用Playwright浏览器自动化获取雪球帖子内容
"""

from playwright.sync_api import sync_playwright
import time
import re
from datetime import datetime
from typing import List, Dict

class XueqiuBrowserAutomation:
    def __init__(self, u_value: str, xq_a_token: str):
        self.u_value = u_value
        self.xq_a_token = xq_a_token
        
    def get_posts(self, max_posts: int = 10) -> List[Dict]:
        """
        获取雪球帖子
        """
        posts = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--no-sandbox', 
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ])
            page = browser.new_page()
            
            # 设置请求头
            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # 设置cookies
            cookies = [
                {'name': 'u', 'value': self.u_value, 'domain': '.xueqiu.com', 'path': '/'},
                {'name': 'xq_a_token', 'value': self.xq_a_token, 'domain': '.xueqiu.com', 'path': '/'}
            ]
            
            page.context.add_cookies(cookies)
            
            try:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 访问雪球首页...")
                page.goto('https://xueqiu.com/', timeout=15000)
                
                # 等待页面加载
                page.wait_for_timeout(3000)
                
                # 查找帖子元素
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 查找帖子元素...")
                
                # 尝试多种选择器
                selectors = ['article', 'div.feed-item', 'div.status-item', 'div.stream-item']
                
                posts_elements = []
                for selector in selectors:
                    try:
                        elements = page.query_selector_all(selector)
                        if elements and len(elements) > 0:
                            posts_elements = elements
                            print(f"   - 使用选择器 '{selector}' 找到 {len(elements)} 个帖子")
                            break
                    except:
                        continue
                
                if not posts_elements:
                    print("   - 未找到帖子元素，尝试通用选择器")
                    posts_elements = page.query_selector_all('div[class*=\"feed\" i], div[class*=\"status\" i], div[class*=\"post\" i]')
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 解析 {len(posts_elements)} 个帖子...")
                
                for i, element in enumerate(posts_elements[:max_posts]):
                    try:
                        # 获取完整的帖子文本内容
                        full_text = element.inner_text()
                        
                        if not full_text or len(full_text.strip()) < 20:
                            continue  # 跳过内容太少的元素
                        
                        # 解析帖子内容
                        parsed_post = self._parse_post(full_text)
                        
                        if parsed_post:
                            parsed_post['index'] = i + 1
                            posts.append(parsed_post)
                            
                    except Exception as e:
                        print(f"   - 解析帖子 {i+1} 时出错: {e}")
                        continue
                        
            except Exception as e:
                print(f"❌ 浏览器自动化过程中出错: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                browser.close()
        
        return posts
    
    def _parse_post(self, full_text: str) -> Dict:
        """
        解析帖子文本内容
        """
        lines = full_text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        # 初始化帖子内容
        post = {
            'title': '无标题',
            'author': '未知作者',
            'content': '',
            'time_info': '',
            'interactions': ''
        }
        
        # 尝试识别各个部分
        author_patterns = [
            r'.*?修改于.*',  # 包含"修改于"的行
            r'.*?·\s*来自.*',  # 包含"· 来自"的行
            r'.*?\d{1,2}:\d{2}.*',  # 包含时间的行
            r'.*?\d{1,2}-\d{1,2}.*'  # 包含日期的行
        ]
        
        content_lines = []
        author_line = ''
        
        for line in lines:
            # 检查是否是作者信息行
            is_author = False
            for pattern in author_patterns:
                if re.search(pattern, line):
                    author_line = line
                    is_author = True
                    break
            
            # 如果不是作者信息，也不是短标题行，则认为是内容
            if not is_author and len(line) > 20:
                content_lines.append(line)
        
        # 设置作者
        if author_line:
            post['author'] = author_line
        
        # 设置内容
        if content_lines:
            post['content'] = ' '.join(content_lines[:5])  # 取前5行内容
        
        # 尝试从内容中提取标题（较短的有意义行）
        for line in lines:
            if 10 < len(line) < 100 and not re.search(r'·\s*来自|修改于|\d{1,2}:\d{2}', line):
                post['title'] = line
                break
        
        # 限制内容长度
        if len(post['content']) > 500:
            post['content'] = post['content'][:500] + '...'
        
        return post
    
    def display_posts(self, posts: List[Dict]):
        """
        显示帖子内容
        """
        if not posts:
            print("❌ 未获取到任何帖子")
            return
        
        print(f"\n📊 获取到 {len(posts)} 个帖子:")
        print("="*80)
        
        for post in posts:
            print(f"\n📈 帖子 {post['index']}:")
            print(f"📝 标题: {post['title']}")
            print(f"👤 作者: {post['author']}")
            print(f"📄 内容: {post['content']}")
            print("-" * 60)

def main():
    print("🎯 雪球浏览器自动化获取器")
    print("="*80)
    
    # 使用提供的凭证
    automation = XueqiuBrowserAutomation(
        u_value="8603655584",
        xq_a_token="17fa2787f256c2057245b461d0c6085a10db6eef"
    )
    
    print("🚀 开始获取雪球帖子...")
    
    # 获取帖子
    posts = automation.get_posts(max_posts=10)
    
    # 显示结果
    automation.display_posts(posts)
    
    print(f"\n✅ 任务完成，共获取 {len(posts)} 个帖子")

if __name__ == "__main__":
    main()