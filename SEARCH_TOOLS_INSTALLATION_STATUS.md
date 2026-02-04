# 搜索工具安装进度

## 当前状态
- 正在安装以下命令行搜索工具：
  1. ripgrep (`rg`) - 超快的行搜索工具
  2. fd (`fd`) - 现代化的find替代品
  3. fzf - 模糊查找工具

## 安装进程
- 安装命令已在后台运行 (`cargo install ripgrep fzf fd-find`)
- 这些工具使用Rust编写，编译安装需要一些时间
- 进程ID: 11266 (ripgrep), 11607 (fzf fd-find)

## 使用说明
一旦安装完成，您将可以使用以下命令：

### ripgrep (`rg`)
```bash
rg "搜索模式" 文件或目录
rg -i "忽略大小写搜索" .
rg --type js "搜索JavaScript文件"
```

### fd
```bash
fd "文件名模式" 搜索目录
fd -t f "*.txt" # 查找txt文件
fd -t d "目录名" # 查找目录
```

### fzf
```bash
# 交互式模糊搜索
find . -type f | fzf
# 或者与其它命令结合使用
fd . ~ | fzf
```

## 验证安装
安装完成后，可通过以下命令验证：
```bash
which rg
which fd  
which fzf
```