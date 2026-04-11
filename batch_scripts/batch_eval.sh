#!/bin/bash

# SBTI批量评测脚本
# 用法1: ./batch_scripts/batch_eval.sh                    # 使用默认模型列表
# 用法2: ./batch_scripts/batch_eval.sh model1 model2 ...   # 使用自定义模型列表

set -e  # 遇到错误立即退出

# 默认模型列表（你可以根据需要修改这个列表）
DEFAULT_MODELS=(
    "openai/gpt-4"
    "openai/gpt-4-turbo"
    "anthropic/claude-3-opus"
    "anthropic/claude-3-sonnet"
    "google/gemini-pro-1.5"
    "meta-llama/llama-3-70b"
    "mistralai/mistral-large"
)

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

# 检查conda环境
if ! conda env list | grep -q "^sbti "; then
    echo "错误: sbti conda环境不存在"
    echo "请先创建环境: conda create -n sbti python=3.10"
    exit 1
fi

# 检查Python依赖（使用conda环境）
echo "检查依赖..."
if ! conda run -n sbti python -c "import requests" 2>/dev/null; then
    echo "错误: sbti环境中的Python依赖未安装"
    echo "请运行: conda activate sbti && pip install -r backend/requirements.txt"
    exit 1
fi

# 使用conda环境的python
PYTHON_CMD="conda run -n sbti python"

# 确定要评测的模型列表
if [ $# -eq 0 ]; then
    # 没有提供参数，使用默认列表
    echo "使用默认模型列表（共 ${#DEFAULT_MODELS[@]} 个模型）"
    echo ""
    echo "默认模型列表:"
    for i in "${!DEFAULT_MODELS[@]}"; do
        echo "  $((i+1)). ${DEFAULT_MODELS[$i]}"
    done
    echo ""
    echo "提示: 你也可以提供自定义模型列表: $0 model1 model2 ..."
    echo ""
    MODELS=("${DEFAULT_MODELS[@]}")
else
    # 提供了参数，使用命令行参数
    echo "使用自定义模型列表（共 $# 个模型）"
    MODELS=("$@")
fi

# 创建data目录
mkdir -p data

# 记录开始时间
START_TIME=$(date +%s)
echo "开始时间: $(date)"
echo ""

# 准备评测
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
    if $PYTHON_CMD -m backend.evaluator "$MODEL_NAME" "$MODEL"; then
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
