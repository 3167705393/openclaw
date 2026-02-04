# file-search Skill

使用新安装的搜索工具（ripgrep, fd, fzf）来帮助用户快速搜索文件和内容。

## 功能
- 使用fd快速查找文件
- 使用ripgrep搜索文件内容
- 使用fzf进行交互式搜索

## 用法
当用户要求搜索文件或内容时激活此Skill：
- "搜索包含X的文件"
- "查找Y文件"
- "在项目中搜索Z"

## 示例
- "搜索所有.js文件" → 使用: fd -e js .
- "查找包含'function'的文件" → 使用: rg "function" .
- "交互式搜索文件" → 使用: fd . | fzf

## 依赖
- ripgrep (rg)
- fd
- fzf