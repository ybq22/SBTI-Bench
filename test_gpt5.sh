#!/bin/bash

# 测试单个模型API调用

echo "=== 测试 GPT-5 API 调用 ==="
echo ""

conda activate sbti

echo "配置信息:"
echo "  模型: openai/gpt-5"
echo "  Max Tokens: 1000"
echo "  Timeout: 120秒"
echo ""

echo "开始测试..."
python -m backend.evaluator "GPT-5测试" "openai/gpt-5"

echo ""
echo "=== 测试完成 ==="
