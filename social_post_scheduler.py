#!/usr/bin/env python3
"""
社交媒体帖子定时推送器
使用cron或其他调度系统定期推送小红书和雪球的帖子
"""

import time
import schedule
import logging
from datetime import datetime
from post_fetcher import SocialMediaPostFetcher

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SocialPostScheduler:
    def __init__(self):
        self.fetcher = SocialMediaPostFetcher()
        self.platform_keywords = {
            "xiaohongshu": ["热门", "生活方式", "美妆", "时尚"],
            "xueqiu": ["热门讨论", "股票", "投资", "市场"]
        }
    
    def fetch_and_push_posts(self, platform: str, keyword: str = ""):
        """
        获取并推送帖子
        """
        try:
            logging.info(f"开始获取 {platform} {keyword} 相关内容")
            
            result = self.fetcher.fetch_posts_with_tavily(platform, keyword)
            
            if "error" in result:
                logging.error(f"获取 {platform} 内容失败: {result['error']}")
                return
            
            summary = result.get("answer", "未获取到摘要")
            sources = result.get("sources", [])
            
            # 这里模拟推送消息（实际应用中会调用message工具）
            print(f"\n📢 [{datetime.now().strftime('%H:%M:%S')}] 推送 {platform} 内容:")
            print(f"🔍 关键词: {keyword or '默认'}")
            print(f"📝 摘要: {summary[:200]}...")
            
            if sources:
                print(f"🔗 来源链接:")
                for i, source in enumerate(sources[:3], 1):  # 只显示前3个来源
                    print(f"  {i}. {source.get('title', '无标题')}")
                    print(f"     {source.get('url', '无链接')}")
            else:
                print("💡 提示: 可以通过以下方式获取更详细内容:")
                if platform == "xiaohongshu":
                    print("   - 访问 https://www.xiaohongshu.com/")
                elif platform == "xueqiu":
                    print("   - 访问 https://xueqiu.com/")
            
            logging.info(f"成功推送 {platform} 内容")
            
        except Exception as e:
            logging.error(f"推送 {platform} 内容时出错: {e}")
    
    def schedule_posts(self):
        """
        设置定时任务
        """
        # 每小时获取一次小红书热门内容
        schedule.every().hour.do(self.fetch_and_push_posts, "xiaohongshu", "热门")
        
        # 每30分钟获取一次雪球热门讨论
        schedule.every(30).minutes.do(self.fetch_and_push_posts, "xueqiu", "热门讨论")
        
        # 每天上午9点推送美妆相关内容
        schedule.every().day.at("09:00").do(self.fetch_and_push_posts, "xiaohongshu", "美妆")
        
        # 每天下午2点推送投资相关内容
        schedule.every().day.at("14:00").do(self.fetch_and_push_posts, "xueqiu", "股票投资")
        
        logging.info("✅ 定时任务已设置完成")
        logging.info("📌 小红书内容将每小时推送一次")
        logging.info("📌 雪球内容将每30分钟推送一次")
        logging.info("📌 美妆内容将在每天上午9点推送")
        logging.info("📌 投资内容将在每天下午2点推送")
    
    def run_scheduler(self):
        """
        运行调度器
        """
        self.schedule_posts()
        
        logging.info("🚀 社交媒体帖子推送服务已启动")
        print("\n💡 说明:")
        print("   - 这个服务会定期推送小红书和雪球的热门内容")
        print("   - 由于访问限制，通过Tavily搜索获取公开信息")
        print("   - 实际部署时，会通过message工具推送给您")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

def main():
    scheduler = SocialPostScheduler()
    
    print("🎯 社交媒体帖子定时推送器")
    print("="*50)
    
    try:
        # 立即运行一次演示
        print("\n🔄 执行一次演示推送...")
        scheduler.fetch_and_push_posts("xiaohongshu", "热门")
        time.sleep(2)
        scheduler.fetch_and_push_posts("xueqiu", "热门讨论")
        
        print(f"\n✅ 演示完成!")
        print("💡 要启动定时推送服务，请运行: python social_post_scheduler.py")
        
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")

if __name__ == "__main__":
    main()