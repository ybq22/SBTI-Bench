#!/bin/bash

# SBTI-Bench 前端服务器启动脚本

echo "================================"
echo "SBTI-Bench 前端服务器"
echo "================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

# 检查数据文件
if [ ! -f "data/results.json" ]; then
    echo "警告: 未找到 data/results.json"
    echo "请先运行评测: python -m backend.evaluator \"Model\" \"model-id\""
    echo ""
fi

# 启动HTTP服务器
PORT=${1:-8000}
echo "项目根目录: $PROJECT_ROOT"
echo "启动HTTP服务器在端口 $PORT..."
echo ""
echo "在浏览器中打开:"
echo "  http://localhost:$PORT/frontend/index.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================"
echo ""

# 使用自定义HTTP服务器（确保UTF-8编码）
python3 server.py $PORT
