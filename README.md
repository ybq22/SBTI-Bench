# SBTI-Bench 前端使用指南

## ⚠️ 重要提示

**不能直接在浏览器中打开 `index.html` 文件！**

由于浏览器的CORS安全限制，如果直接双击打开HTML文件（`file://` 协议），JavaScript 无法读取本地的 JSON 文件。

## ✅ 正确的使用方法

### 方法1：使用启动脚本（推荐）

```bash
# 在项目根目录运行
./start_server.sh
```

然后在浏览器中打开：`http://localhost:8000/frontend/index.html`

### 方法2：手动启动HTTP服务器

```bash
# 在项目根目录运行
python3 -m http.server 8000
```

然后在浏览器中打开：`http://localhost:8000/frontend/index.html`

### 方法3：使用其他HTTP服务器

**如果安装了 Node.js：**
```bash
npx serve
# 或
npx http-server -p 8000
```

**如果安装了 Python 2：**
```bash
python -m SimpleHTTPServer 8000
```

## 🔧 诊断工具

如果前端无法正常显示，请使用诊断工具：

1. 启动HTTP服务器（见上面的方法）
2. 在浏览器中打开：`http://localhost:8000/frontend/diagnose.html`
3. 按照页面提示检查和修复问题

## 📋 常见问题

### Q1: 为什么不能直接打开HTML文件？

**A:** 现代浏览器的安全策略禁止 `file://` 协议下的网页使用 `fetch()` 读取本地文件。这是为了防止恶意网页访问你的本地文件。

### Q2: 前端显示"无法加载数据"怎么办？

**A:** 请按以下步骤检查：

1. **确认HTTP服务器已启动**
   ```bash
   # 在浏览器中访问
   http://localhost:8000/data/results.json
   ```
   如果能看到JSON数据，说明服务器正常。

2. **确认数据文件存在**
   ```bash
   ls -la data/results.json
   ```

3. **使用诊断工具**
   ```
   http://localhost:8000/frontend/diagnose.html
   ```

### Q3: 如何修改前端页面？

编辑 `frontend/index.html` 文件，然后刷新浏览器即可看到更改。

### Q4: 端口8000被占用怎么办？

```bash
# 使用其他端口
./start_server.sh 8080
# 或
python3 -m http.server 8080
```

然后访问 `http://localhost:8080/frontend/index.html`

### Q5: 如何停止HTTP服务器？

在运行服务器的终端窗口按 `Ctrl + C`

## 🌐 在局域网中访问

如果想让其他设备访问你的前端页面：

```bash
# 使用你的IP地址启动服务器
python3 -m http.server 8000 --bind 0.0.0.0
```

然后其他设备可以通过 `http://你的IP地址:8000/frontend/index.html` 访问。

## 📱 移动设备访问

1. 确保电脑和手机在同一个WiFi网络
2. 在电脑上启动HTTP服务器并绑定到所有接口
3. 在手机浏览器中访问电脑的IP地址

## 🔒 安全提示

- HTTP服务器仅用于本地开发，不要在生产环境使用
- 不要在公网环境暴露HTTP服务器端口
- 定期清理 `data/results.json` 中的敏感信息
