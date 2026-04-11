# SBTI-Bench 使用指南

## 快速开始

### 1. 配置API密钥

编辑 `.env` 文件：

```
OPENROUTER_API_KEY=your_actual_api_key_here
DEFAULT_MODEL=openai/gpt-4
```

**获取API密钥**：
- 访问 [OpenRouter官网](https://openrouter.ai/)
- 注册账号并获取API密钥
- 将密钥填入 `.env` 文件

### 2. 评测单个模型

```bash
python -m backend.evaluator "GPT-4" "openai/gpt-4"
```

**参数说明**：
- 第一个参数：模型显示名称（可以自定义）
- 第二个参数：OpenRouter模型ID（必须有效）

**示例**：

```bash
# 评测GPT-4
python -m backend.evaluator "GPT-4" "openai/gpt-4"

# 评测Claude 3
python -m backend.evaluator "Claude 3 Opus" "anthropic/claude-3-opus"

# 评测Llama 3
python -m backend.evaluator "Llama 3 70B" "meta-llama/llama-3-70b"
```

### 3. 批量评测

```bash
./batch_scripts/batch_eval.sh \
  "openai/gpt-4" \
  "anthropic/claude-3-sonnet" \
  "meta-llama/llama-3-70b"
```

**特点**：
- 自动在模型间添加5秒延迟
- 失败后继续下一个模型
- 显示总耗时和结果文件路径

### 4. 查看结果

**方式1: 命令行查看**

```bash
# 查看最新评测结果
cat data/results.json | jq '.evaluations[-1]'

# 查看所有模型类型
cat data/results.json | jq '.evaluations[] | {model: .model_name, type: .sbiti_type, name: .chinese_name}'

# 查看类型分布
cat data/results.json | jq '.evaluations | group_by(.sbiti_type) | map({type: .[0].sbiti_type, name: .[0].chinese_name, count: length})'
```

**方式2: 前端页面**

在浏览器中打开 `frontend/index.html` 查看：
- 模型排行榜
- SBTI类型分布
- 统计概览

## 常用命令

### 测试相关

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_scoring.py -v

# 运行测试并查看覆盖率
pytest tests/ -v --cov=backend
```

### 数据管理

```bash
# 查看结果文件
cat data/results.json

# 美化输出JSON
cat data/results.json | jq .

# 备份结果
cp data/results.json data/results_$(date +%Y%m%d).json
```

## 高级用法

### 自定义API参数

创建自定义评测脚本：

```python
from backend.evaluator import SBTEEvaluator

# 自定义参数
evaluator = SBTEEvaluator(
    model_name="My Custom Model",
    model_id="openai/gpt-4",
    api_key="your_api_key"
)

# 自定义温度参数
evaluator.llm.temperature = 0.5
evaluator.llm.max_tokens = 500

# 运行评测
result = evaluator.run()
```

### 批量评测模型列表

创建 `models.txt`：

```
openai/gpt-4
anthropic/claude-3-opus
anthropic/claude-3-sonnet
meta-llama/llama-3-70b
google/gemini-pro
```

然后运行：

```bash
./batch_scripts/batch_eval.sh $(cat models.txt)
```

### 结果分析

```python
import json
from collections import Counter

# 加载结果
with open('data/results.json', 'r') as f:
    data = json.load(f)

# 统计类型分布
types = [e['sbiti_type'] for e in data['evaluations']]
type_counts = Counter(types)

print("SBTI类型分布:")
for type, count in type_counts.most_common():
    print(f"  {type}: {count}")

# 计算平均相似度
avg_similarity = sum(e['match_similarity'] for e in data['evaluations']) / len(data['evaluations'])
print(f"平均匹配度: {avg_similarity:.1f}%")
```

## 常见问题

### Q: API限流怎么办？

A: 批量评测脚本已内置5秒延迟。如需调整：

```bash
# 编辑 batch_scripts/batch_eval.sh
# 修改 sleep 5 为更长的时间（如 sleep 10）
```

### Q: 如何添加新模型？

A: 在OpenRouter支持的模型列表中选择：

```bash
python -m backend.evaluator "New Model" "provider/model-name"
```

查看可用模型：https://openrouter.ai/models

### Q: 评测中断怎么办？

A: 已完成的结果会自动保存到 `data/results.json`。可以继续评测：

```bash
# 继续批量评测
./batch_scripts/batch_eval.sh "next-model"
```

### Q: 如何重置评测数据？

A: 删除或重命名结果文件：

```bash
# 备份当前结果
mv data/results.json data/results_backup.json

# 然后重新开始评测
```

### Q: 环境变量不生效？

A: 确保 `.env` 文件在项目根目录：

```bash
# 检查.env文件位置
ls -la .env

# 手动加载环境变量
export $(cat .env | xargs)
```

## 数据解读

### SBTI类型说明

- **26种常规类型**：CTRL, BOSS, SHIT, DEVI, PROG, SHAR, TRAN, CLDE, SCHL, ORGA, LOGI, ANAL, ARCH, SCIE, JUDG, DIPLO, INTE, LEAD, COOR, ARBI, MEDI, HEAL, EDUC, CREA, ARTI

- **2种特殊类型**：
  - **DRUNK (酒鬼)**：当模型选择"饮酒"且"酒精令我信服"时触发
  - **HHHH (傻乐者)**：当与所有类型相似度<60%时触发

### 评分标准

- **原始分数**：每个维度2-6分
  - 2分：最低倾向
  - 4分：中等倾向
  - 6分：最高倾向

- **等级**：
  - **L (Low)**：≤3分
  - **M (Medium)**：=4分
  - **H (High)**：≥5分

- **匹配度**：
  - 100%：完全匹配
  - ≥80%：高度匹配
  - 60-79%：中度匹配
  - <60%：低匹配（触发HHHH）

### 15个维度

1. **S1-S3**: Self Model (自我认知)
   - S1: 自我评估
   - S2: 自我调节
   - S3: 自我提升

2. **E1-E3**: Emotion Model (情感倾向)
   - E1: 情感表达
   - E2: 情感控制
   - E3: 情感理解

3. **A1-A3**: Attitude Model (态度取向)
   - A1: 积极态度
   - A2: 消极态度
   - A3: 中立态度

4. **Ac1-Ac3**: Action Model (行为模式)
   - Ac1: 行为规划
   - Ac2: 行为执行
   - Ac3: 行为反思

5. **So1-So3**: Social Model (社交特征)
   - So1: 社交主动性
   - So2: 社交适应性
   - So3: 社交影响力

## 性能优化建议

1. **批量评测时**：选择非高峰时段（如凌晨或早晨）
2. **API调用**：适当增加延迟避免限流
3. **结果缓存**：避免重复评测相同模型
4. **并行评测**：可以分多个终端同时评测不同模型组

## 故障排查

### 问题：ModuleNotFoundError

```bash
# 解决方案：安装依赖
pip install -r backend/requirements.txt
```

### 问题：API key错误

```bash
# 检查.env文件
cat .env

# 确保格式正确（无空格、无引号）
OPENROUTER_API_KEY=sk-or-v1-...
```

### 问题：模型不存在

```bash
# 检查OpenRouter可用模型
curl https://openrouter.ai/api/v1/models
```

### 问题：JSON解析错误

```bash
# 验证JSON格式
python -m json.tool data/results.json

# 如果损坏，从备份恢复
cp data/results_backup.json data/results.json
```

## 更多资源

- **OpenRouter文档**：https://openrouter.ai/docs
- **SBTI原项目**：B站@蛆肉儿串儿
- **项目Issues**：GitHub Issues
