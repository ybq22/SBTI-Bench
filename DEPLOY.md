# GitHub Pages 部署指南

## 自动部署

本项目已配置 GitHub Actions，当代码推送到 `main` 分支时会自动部署到 GitHub Pages。

### 首次设置步骤

1. **启用 GitHub Pages**
   - 进入仓库的 **Settings** > **Pages**
   - 在 "Build and deployment" > **Source** 中选择 **GitHub Actions**

2. **推送代码**
   ```bash
   git add .
   git commit -m "配置GitHub Pages部署"
   git push origin main
   ```

3. **查看部署状态**
   - 进入仓库的 **Actions** 标签页
   - 查看 "Deploy to GitHub Pages" 工作流的运行状态

4. **访问网站**
   - 部署成功后，访问 `https://<你的用户名>.github.io/SBTI-Bench/`

### 自动触发条件

部署会在以下情况自动触发：
- 推送到 `main` 分支
- 修改了以下目录的文件：
  - `frontend/`
  - `data/`
  - `image/`
  - `.github/workflows/deploy.yml`

### 手动触发部署

1. 进入仓库的 **Actions** 标签页
2. 选择 "Deploy to GitHub Pages" 工作流
3. 点击 **Run workflow** 按钮

## 路径配置

前端代码已实现智能路径检测，会自动适配：
- ✅ 本地开发环境 (`http://localhost:8000/frontend/index.html`)
- ✅ GitHub Pages (`https://username.github.io/SBTI-Bench/`)
- ✅ 自定义域名

## 文件结构

部署到 GitHub Pages 的文件结构：
```
SBTI-Bench/
├── frontend/
│   └── index.html
├── data/
│   └── results.json
└── image/
    └── *.jpg
```

## 更新数据

当有新的评测结果时：

1. **更新数据文件**
   ```bash
   python -m backend.evaluator "Model" "model-id"
   ```

2. **提交并推送**
   ```bash
   git add data/results.json
   git commit -m "更新评测数据"
   git push origin main
   ```

3. **等待自动部署**
   - GitHub Actions 会自动触发部署
   - 大约 1-2 分钟后网站会更新

## 本地预览

在本地预览网站效果：

```bash
# 使用提供的启动脚本
./start_server.sh

# 或指定端口
./start_server.sh 8080
```

然后在浏览器中打开 `http://localhost:8000/frontend/index.html`

## 故障排查

### 网站无法访问

1. 检查 GitHub Pages 是否已启用
2. 确认 Source 设置为 "GitHub Actions"
3. 查看 Actions 工作流是否成功运行

### 数据无法加载

1. 确认 `data/results.json` 文件存在
2. 检查浏览器控制台是否有错误信息
3. 确认文件已提交到 GitHub 仓库

### 图片无法显示

1. 确认 `image/` 目录已提交到仓库
2. 检查图片文件名是否正确（区分大小写）
3. 查看 Actions 部署日志

## 自定义域名（可选）

如果需要使用自定义域名：

1. 在仓库的 **Settings** > **Pages** > **Custom domain** 中设置域名
2. 在域名 DNS 设置中添加 CNAME 记录指向 `<你的用户名>.github.io`
3. 等待 DNS 生效（可能需要几分钟到几小时）

## 性能优化

- 首次加载可能需要 2-3 秒
- GitHub Pages 有一定的缓存时间
- 建议使用 CDN 加速（如需要）

## 安全注意事项

- ⚠️ `.env` 文件包含 API 密钥，**不要**提交到仓库
- ⚠️ 评测数据会公开显示在网站上
- ✅ 仅包含静态文件，无后端服务，安全性较高
