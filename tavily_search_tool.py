#!/usr/bin/env python3
"""
Tavily搜索工具
使用Tavily API进行智能网络搜索
"""

import os
import requests
import json
from typing import Dict, List, Optional

class TavilySearchTool:
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化Tavily搜索工具
        :param api_key: Tavily API密钥，如果不提供则从环境变量获取
        """
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            raise ValueError("Tavily API密钥未设置。请设置TAVILY_API_KEY环境变量。")
        
        self.base_url = "https://api.tavily.com/search"
    
    def search(
        self,
        query: str,
        search_depth: str = "basic",
        include_answer: bool = True,
        include_sources: bool = True,
        max_results: int = 5,
        include_images: bool = False,
        include_raw_content: bool = False
    ) -> Dict:
        """
        执行Tavily搜索
        :param query: 搜索查询
        :param search_depth: 搜索深度 ("basic" 或 "advanced")
        :param include_answer: 是否包含AI生成的答案
        :param include_sources: 是否包含来源
        :param max_results: 最大结果数量
        :param include_images: 是否包含图片
        :param include_raw_content: 是否包含原始内容
        :return: 搜索结果
        """
        payload = {
            "query": query,
            "api_key": self.api_key,
            "search_depth": search_depth,
            "include_answer": include_answer,
            "include_sources": include_sources,
            "max_results": max_results,
            "include_images": include_images,
            "include_raw_content": include_raw_content
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"搜索请求失败: {str(e)}"}
        except Exception as e:
            return {"error": f"搜索过程中发生错误: {str(e)}"}

def main():
    """命令行接口示例"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python tavily_search_tool.py <搜索查询>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    
    try:
        tool = TavilySearchTool()
        result = tool.search(query)
        
        if "error" in result:
            print(f"搜索失败: {result['error']}")
        else:
            if result.get("answer"):
                print(f"摘要: {result['answer']}\n")
            
            print("搜索结果:")
            for i, source in enumerate(result.get("sources", []), 1):
                print(f"{i}. {source.get('title', '无标题')}")
                print(f"   链接: {source.get('url', 'N/A')}")
                print(f"   内容: {source.get('content', 'N/A')[:200]}...")
                print()

    except ValueError as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()