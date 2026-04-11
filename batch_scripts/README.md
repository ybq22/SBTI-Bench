# 批量评测脚本使用说明

## 快速开始

### 方法1：使用配置文件（推荐）

```bash
# 编辑 batch_scripts/models.conf 文件，添加你想评测的模型
# 然后直接运行：
./batch_scripts/batch_eval.sh
```

### 方法2：使用内置默认列表

```bash
# 删除或重命名 models.conf，脚本会使用内置的7个默认模型
./batch_scripts/batch_eval.sh
```

### 方法3：命令行指定模型

```bash
# 提供自定义模型列表
./batch_scripts/batch_eval.sh "openai/gpt-4" "anthropic/claude-3-opus"
```

## 配置文件格式

创建或编辑 `batch_scripts/models.conf`：

```bash
# 注释行以 # 开头
# 每行一个模型，格式: provider/model-name

# OpenAI
openai/gpt-4
openai/gpt-4-turbo

# Anthropic
anthropic/claude-3-opus
anthropic/claude-3-sonnet

# Google
google/gemini-pro-1.5
```

## 优先级

1. **命令行参数** > 2. **配置文件** > 3. **内置默认列表**

示例：
```bash
# 即使配置文件中有10个模型，这行命令只会评测这2个
./batch_scripts/batch_eval.sh "model1" "model2"
```

## 常用模型列表

### 闭源商业模型
- `openai/gpt-4`
- `openai/gpt-4-turbo`
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `google/gemini-pro-1.5`

### 开源模型
- `meta-llama/llama-3-70b`
- `meta-llama/llama-3-8b`
- `mistralai/mistral-large`
- `huggingfaceh4/zephyr-7b-beta`

### 中国模型
- `z-ai/glm-5.1`
- `01-ai/yi-large`
- `deepseek/deepseek-chat`

## 注意事项

1. **API密钥**：确保 `.env` 文件中配置了有效的 `OPENROUTER_API_KEY`
2. **网络**：评测过程需要稳定的网络连接
3. **时间**：每个模型大约需要1-3分钟，取决于网络速度
4. **限流**：脚本会在模型间自动等待5秒，避免API限流
5. **成本**：请注意API调用费用，建议先用小模型测试

## 查看可用模型

访问 [OpenRouter Models](https://openrouter.ai/models) 查看所有可用的模型。

## 故障排查

### 问题：依赖未安装
```bash
conda activate sbti
pip install -r backend/requirements.txt
```

### 问题：conda环境不存在
```bash
conda create -n sbti python=3.10
conda activate sbti
pip install -r backend/requirements.txt
```

### 问题：API限流
编辑 `batch_scripts/batch_eval.sh`，增加延迟时间：
```bash
sleep 10  # 改为10秒
```

### 问题：单个模型失败
脚本会继续评测下一个模型，失败的模型不会影响其他模型。
