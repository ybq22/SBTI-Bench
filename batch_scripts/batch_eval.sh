#!/bin/bash

# SBTI批量评测脚本
# 用法: ./batch_scripts/batch_eval.sh model1 model2 model3 ...

set -e  # 遇到错误立即退出

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "================================"
echo "SBTI批量评测脚本"
echo "================================"
echo "项目根目录: $PROJECT_ROOT"
echo ""

# 检查环境变量
if [ ! -f .env ]; then
    echo "错误: .env文件不存在"
    echo "请从.env.example复制并配置API密钥"
    exit 1
fi

# 检查Python依赖
if ! python3 -c "import requests" 2>/dev/null; then
    echo "错误: Python依赖未安装"
    echo "请运行: pip install -r backend/requirements.txt"
    exit 1
fi

# 检查参数
if [ $# -eq 0 ]; then
    echo "错误: 请提供至少一个模型名称"
    echo "用法: $0 model1 [model2] [model3] ..."
    echo ""
    echo "示例:"
    echo "  $0 openai/gpt-4"
    echo "  $0 openai/gpt-4 anthropic/claude-3-opus"
    echo "  $0 gpt-4 claude-opus llama-3-70b"
    exit 1
fi

# 创建data目录
mkdir -p data

# 记录开始时间
START_TIME=$(date +%s)
echo "开始时间: $(date)"
echo ""

# 逐个评测模型
MODELS=("$@")
TOTAL=${#MODELS[@]}
CURRENT=0

for MODEL in "${MODELS[@]}"; do
    CURRENT=$((CURRENT + 1))
    echo ""
    echo "================================"
    echo "[$CURRENT/$TOTAL] 正在评测: $MODEL"
    echo "================================"

    # 生成模型名称（去除路径和特殊字符）
    MODEL_NAME=$(basename "$MODEL" | sed 's/[^a-zA-Z0-9_-]/_/g')

    # 运行评测
    if python3 -m backend.evaluator "$MODEL_NAME" "$MODEL"; then
        echo "✓ $MODEL 评测完成"
    else
        echo "✗ $MODEL 评测失败"
        echo "继续下一个模型..."
    fi

    # 添加延迟避免API限流
    if [ $CURRENT -lt $TOTAL ]; then
        echo ""
        echo "等待5秒后继续..."
        sleep 5
    fi
done

# 计算耗时
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

echo ""
echo "================================"
echo "批量评测完成！"
echo "================================"
echo "总模型数: $TOTAL"
echo "总耗时: ${MINUTES}分${SECONDS}秒"
echo "结果文件: data/results.json"
echo ""
echo "查看结果: cat data/results.json"
