# 雪球登录凭证获取指南

## 为什么需要登录凭证

要获取雪球的完整帖子内容，特别是那些需要登录才能查看的内容，我们需要使用登录凭证（cookies）。

## 如何获取登录凭证

### 方法一：浏览器开发者工具（推荐）

1. **登录雪球网站**
   - 访问 https://xueqiu.com/
   - 使用您的账号登录

2. **打开开发者工具**
   - 按 F12 或右键选择"检查"
   - 选择"Network"（网络）标签

3. **获取Cookies**
   - 刷新页面
   - 点击任意网络请求
   - 在Headers（请求头）中找到Cookie字段
   - 复制整个Cookie值

4. **提取关键Cookie**
   - 重点关注 `xq_a_token` 和 `u` 等字段
   - 这些是访问雪球API的关键凭证

### 方法二：使用浏览器扩展

1. 安装"EditThisCookie"或类似扩展
2. 访问雪球网站
3. 使用扩展导出Cookies

## 如何使用登录凭证

将获取的Cookie信息提供给爬取器：

```python
cookies = {
    'xq_a_token': 'your_token_here',
    'u': 'your_user_id',
    # 其他cookie字段
}

scraper = XueqiuScraper(cookies=cookies)
posts = scraper.search_topics('热门话题')
```

## 安全注意事项

- 不要在公共场合分享您的登录凭证
- 定期更换密码
- 注意保护个人隐私信息

## 技术实现

提供的 `xueqiu_scraper.py` 脚本可以使用登录凭证来获取完整的帖子内容，包括：
- 帖子全文
- 用户评论
- 点赞和转发信息
- 更多详细数据