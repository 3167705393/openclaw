# Tavily API密钥配置更新说明

## 问题
之前的API密钥包含空格（tvly-dev-jV0bOhEvpw v9PuwRkdyjihvXQsiCp2Tp），这不是有效的API密钥格式。

## 正确的API密钥格式
Tavily API密钥应该是一个连续的字符串，类似：
- tvly_dev_jV0bOhEvpwv9PuwRkdyjihvXQsiCp2Tp
- 或 tvly-QWERTY1234567890abcdef

## 重新配置步骤
1. 获取正确的API密钥（从 https://www.tavily.com/）
2. 确保API密钥是连续的，没有空格
3. 使用以下命令设置：
   ```bash
   export TAVILY_API_KEY="your_correct_api_key_here"
   echo 'export TAVILY_API_KEY="your_correct_api_key_here"' >> ~/.bashrc
   ```

## 验证API密钥
使用以下Python代码验证API密钥：
```python
import requests
import os

api_key = os.environ.get('TAVILY_API_KEY')
if api_key:
    url = 'https://api.tavily.com/search'
    data = {
        'api_key': api_key,
        'query': 'test',
        'max_results': 1
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ API密钥有效")
    else:
        print("❌ API密钥无效或缺失")
        print(response.json())
```

## 注意事项
- API密钥区分大小写
- 不要在公共场合暴露API密钥
- 定期更换API密钥以保证安全