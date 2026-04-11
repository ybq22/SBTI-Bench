#!/bin/bash

# SBTI批量评测脚本
# 用法1: ./batch_scripts/batch_eval.sh                    # 使用配置文件或默认模型列表（跳过已评测）
# 用法2: ./batch_scripts/batch_eval.sh --force            # 强制重新评测所有模型
# 用法3: ./batch_scripts/batch_eval.sh model1 model2 ...   # 使用自定义模型列表

set -e  # 遇到错误立即退出

# 配置文件路径
CONFIG_FILE="$(dirname "${BASH_SOURCE[0]}")/models.conf"

# 默认模型列表（当配置文件不存在时使用）
DEFAULT_MODELS=(
    "openai/gpt-4"
    "openai/gpt-4-turbo"
    "anthropic/claude-3-opus"
    "anthropic/claude-3-sonnet"
    "google/gemini-pro-1.5"
    "meta-llama/llama-3-70b"
    "mistralai/mistral-large"
)

# 命令行参数
FORCE_REEVAL=false  # 是否强制重新评测
SKIP_EXISTING=true  # 是否跳过已评测的模型（默认）

# 从配置文件加载模型列表
load_models_from_config() {
    local config_file="$1"
    local models=()

    if [ -f "$config_file" ]; then
        # 读取配置文件，过滤空行和注释
        while IFS= read -r line || [ -n "$line" ]; do
            # 去除首尾空格
            line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

            # 跳过空行和注释
            if [ -n "$line" ] && [[ ! "$line" =~ ^# ]]; then
                models+=("$line")
            fi
        done < "$config_file"
    fi

    echo "${models[@]}"
}

# 检查模型是否已经被评测过
is_model_evaluated() {
    local model_id="$1"
    local results_file="data/results.json"

    if [ ! -f "$results_file" ]; then
        return 1  # 文件不存在，未评测
    fi

    # 使用Python检查JSON中是否存在该model_id
    local result=$(python3 -c "
import json
import sys
try:
    with open('$results_file', 'r') as f:
        data = json.load(f)

    for eval_data in data['evaluations']:
        if eval_data['model_id'] == '$model_id':
            print('FOUND')
            sys.exit(0)

    print('NOT_FOUND')
    sys.exit(1)
except Exception as e:
    print('ERROR')
    sys.exit(2)
" 2>/dev/null)

    [ "$result" = "FOUND" ]
}

# 显示已评测的模型列表
show_evaluated_models() {
    local results_file="data/results.json"

    if [ ! -f "$results_file" ]; then
        echo "  尚未有任何评测结果"
        return
    fi

    local count=$(python3 -c "
import json
with open('$results_file', 'r') as f:
    data = json.load(f)
print(len(data['evaluations']))
" 2>/dev/null || echo "0")

    echo "  已评测 $count 个模型:"
    python3 -c "
import json
with open('$results_file', 'r') as f:
    data = json.load(f)
for eval_data in data['evaluations']:
    print(f\"    • {eval_data['model_name']} ({eval_data['model_id']})\")
" 2>/dev/null || echo "  无法读取评测结果"
}

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
# 解析命令行参数
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE_REEVAL=true
            shift
            ;;
        --no-skip)
            SKIP_EXISTING=false
            shift
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

if [ ${#ARGS[@]} -eq 0 ]; then
    # 没有提供参数，尝试从配置文件加载
    CONFIG_MODELS=($(load_models_from_config "$CONFIG_FILE"))

    if [ ${#CONFIG_MODELS[@]} -gt 0 ]; then
        # 配置文件存在且有模型
        MODELS=("${CONFIG_MODELS[@]}")
    else
        # 配置文件不存在或为空，使用默认列表
        MODELS=("${DEFAULT_MODELS[@]}")
    fi
else
    # 提供了参数，使用命令行参数
    MODELS=("${ARGS[@]}")
fi

# 显示评测模式
echo "================================"
echo "批量评测配置"
echo "================================"
if [ "$FORCE_REEVAL" = true ]; then
    echo "模式: 强制重新评测所有模型 (--force)"
else
    echo "模式: 跳过已评测的模型 (默认)"
    echo "      使用 --force 强制重新评测"
fi

if [ ${#MODELS[@]} -eq 0 ]; then
    echo ""
    echo "错误: 没有要评测的模型"
    exit 1
fi

echo ""
echo "待评测模型列表（共 ${#MODELS[@]} 个）:"
for i in "${!MODELS[@]}"; do
    MODEL="${MODELS[$i]}"
    if is_model_evaluated "$MODEL"; then
        echo "  $((i+1)). $MODEL [已评测，将跳过]"
    else
        echo "  $((i+1)). $MODEL"
    fi
done

echo ""
show_evaluated_models
echo ""
echo "================================"
echo ""

# 创建data目录
mkdir -p data

# 记录开始时间
START_TIME=$(date +%s)
echo "开始时间: $(date)"
echo ""

# 准备评测
TOTAL=${#MODELS[@]}
CURRENT=0

# 统计实际需要评测的模型
NEED_EVAL=0
for MODEL in "${MODELS[@]}"; do
    if [ "$FORCE_REEVAL" = true ] || ! is_model_evaluated "$MODEL"; then
        NEED_EVAL=$((NEED_EVAL + 1))
    fi
done

echo "开始时间: $(date)"
echo "需要评测: $NEED_EVAL / ${#MODELS[@]} 个模型"
echo ""

# 逐个评测模型
TOTAL=${#MODELS[@]}
CURRENT=0
COMPLETED=0
SKIPPED=0

for MODEL in "${MODELS[@]}"; do
    CURRENT=$((CURRENT + 1))

    # 检查是否已评测
    if [ "$FORCE_REEVAL" = false ] && is_model_evaluated "$MODEL"; then
        echo "[$CURRENT/$TOTAL] ⊞ 跳过已评测: $MODEL"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    COMPLETED=$((COMPLETED + 1))
    echo ""
    echo "================================"
    echo "[$CURRENT/$TOTAL] [$COMPLETED/$NEED_EVAL] 正在评测: $MODEL"
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
echo "已评测: $COMPLETED"
echo "跳过: $SKIPPED"
echo "总耗时: ${MINUTES}分${SECONDS}秒"
echo "结果文件: data/results.json"
echo ""
echo "查看结果:"
echo "  cat data/results.json | jq '.evaluations | length'"
echo "  或打开: http://localhost:8001/frontend/index.html"
echo ""
echo "提示: 使用 --force 可强制重新评测所有模型"
