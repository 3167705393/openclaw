# Tavily API 配置示例

## 获取API密钥
1. 访问 https://www.tavily.com/
2. 注册账户并获取API密钥
3. API密钥可在账户仪表板中找到

## 环境变量配置
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export TAVILY_API_KEY="your_tavily_api_key_here"
```

## OpenClaw配置
如果需要在OpenClaw中配置API密钥：
```bash
# 使用OpenClaw配置工具
openclaw configure --section api --key TAVILY_API_KEY --value "your_api_key_here"
```

## 使用示例
```javascript
// 在skill中使用
const { TavilySearchTool } = require('./tavily_search_tool');

const tavily = new TavilySearchTool(process.env.TAVILY_API_KEY);
const results = await tavily.search("最新的AI发展");
```

## API限制
- 免费账户: 每月1000次请求
- 速率限制: 每秒1个请求
- 查询长度限制: 2000字符

## 错误处理
常见错误代码:
- 401: 无效API密钥
- 429: 请求过于频繁
- 500: 服务器错误

## 安全提示
- 不要在代码中硬编码API密钥
- 定期更换API密钥
- 限制API密钥的使用范围