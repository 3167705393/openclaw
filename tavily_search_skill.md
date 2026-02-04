# tavily-search Skill

使用Tavily API进行智能网络搜索，提供准确、最新和经过审核的信息。

## 功能
- 实时网络搜索
- 来源引用和链接
- 多样化搜索结果
- 事实核查

## 依赖
- Tavily API密钥
- Python 3.x (requests, json模块)

## 触发条件
当用户需要获取最新信息、进行研究或需要引用来源时激活此Skill：
- "搜索X的最新信息"
- "查找关于Y的信息"
- "帮我调查Z"
- "获取最新新闻"
- "查找数据统计"

## 使用方法
1. 从Tavily获取API密钥 (https://www.tavily.com/)
2. 配置API密钥到系统环境变量
3. 使用时调用Tavily API进行搜索

## 示例
```python
import requests
import json

def tavily_search(query, api_key):
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "api_key": api_key,
        "search_depth": "advanced",  # 或 "basic"
        "include_answer": True,
        "include_sources": True,
        "max_results": 5
    }
    
    response = requests.post(url, json=payload)
    return response.json()
```

## 参数说明
- `search_depth`: "basic" 或 "advanced" - 影响搜索质量和时间
- `include_answer`: True/False - 是否包含AI生成的答案摘要
- `include_sources`: True/False - 是否包含来源链接
- `max_results`: 最大返回结果数
- `include_images`: True/False - 是否包含图片
- `include_raw_content`: True/False - 是否包含原始内容

## 注意事项
- 需要有效的Tavily API密钥
- 遵守API使用频率限制
- 结果可能因搜索深度而异