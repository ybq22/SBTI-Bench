# SBTI-Bench: 大模型SBTI人格评测基准

将真人SBTI测试系统改造为大模型评测基准，通过标准化测试评估不同AI模型的"人格"特征。

## 项目特点

- 支持26种SBTI人格类型
- 15个维度全面评估
- OpenRouter API统一调用
- 批量评测支持
- 可视化结果展示

## 快速开始

### 1. 安装依赖

```bash
pip install -r backend/requirements.txt
```

### 2. 配置API密钥

```bash
cp .env.example .env
# 编辑.env文件，添加你的OpenRouter API密钥
```

编辑 `.env` 文件：

```
OPENROUTER_API_KEY=your_actual_api_key_here
DEFAULT_MODEL=openai/gpt-4
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000
```

### 3. 评测单个模型

```bash
python -m backend.evaluator "GPT-4" "openai/gpt-4"
```

### 4. 批量评测

```bash
./batch_scripts/batch_eval.sh \
  "openai/gpt-4" \
  "anthropic/claude-3-opus" \
  "meta-llama/llama-3-70b"
```

### 5. 查看结果

**方式1: 直接查看JSON**

```bash
cat data/results.json | jq '.evaluations[-1]'
```

**方式2: 打开前端页面**

在浏览器中打开 `frontend/index.html` 查看可视化排行榜。

## 项目结构

```
SBTI-Bench/
├── backend/              # Python后端
│   ├── questions.py     # SBTI问题数据
│   ├── scoring.py       # 计分逻辑
│   ├── matcher.py       # 类型匹配算法
│   ├── llm_interface.py # OpenRouter API接口
│   └── evaluator.py     # 主评测脚本
├── batch_scripts/        # 批量脚本
│   └── batch_eval.sh    # 批量评测脚本
├── data/                # 评测数据
│   └── results.json     # 评测结果
├── frontend/            # 前端展示
│   └── index.html       # 结果展示页面
├── image/               # SBTI类型图片
├── tests/               # 单元测试
└── README.md            # 项目文档
```

## SBTI类型

本系统支持26种SBTI人格类型：

- **CTRL** (拿捏者) - 控制型人格
- **BOSS** (领导者) - 领导型人格
- **SHIT** (愤世者) - 批判型人格
- **DRUNK** (酒鬼) - 特殊类型：酒精触发
- **HHHH** (傻乐者) - 特殊类型：兜底类型
- 以及其他21种类型...

## 评测原理

1. **30个问题**覆盖15个维度：
   - Self Model (S1-S3): 自我认知
   - Emotion Model (E1-E3): 情感倾向
   - Attitude Model (A1-A3): 态度取向
   - Action Model (Ac1-Ac3): 行为模式
   - Social Model (So1-So3): 社交特征

2. **维度评分**：每个维度2-6分，转换为L/M/H三个等级

3. **向量匹配**：使用曼哈顿距离算法找到最相似的SBTI类型

4. **特殊类型**：
   - **DRUNK**：当用户选择"饮酒"且"酒精令我信服"时触发
   - **HHHH**：当与所有类型相似度<60%时触发

## 结果数据结构

```json
{
  "last_updated": "2025-04-10T12:00:00",
  "total_evaluations": 3,
  "evaluations": [
    {
      "model_name": "GPT-4",
      "model_id": "openai/gpt-4",
      "evaluation_date": "2025-04-10T12:00:00",
      "sbiti_type": "CTRL",
      "chinese_name": "拿捏者",
      "pattern": "HHH-HMH-MHH-HHH-MHM",
      "match_similarity": 95,
      "exact_dimensions": 12,
      "raw_scores": {
        "S1": 6,
        "S2": 4,
        ...
      },
      "levels": {
        "S1": "H",
        "S2": "M",
        ...
      },
      "is_special": false,
      "drunk_triggered": false,
      "api_params": {
        "model": "openai/gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
      }
    }
  ]
}
```

## 开发

### 运行测试

```bash
pytest tests/ -v
```

### 运行测试（带覆盖率）

```bash
pytest tests/ -v --cov=backend
```

### 添加新的评测维度

1. 在 `backend/questions.py` 中定义问题和选项
2. 在 `backend/scoring.py` 中添加计分逻辑
3. 运行测试确保正确性

## 常见问题

### API限流怎么办？

批量评测脚本已内置5秒延迟，如需调整，编辑 `batch_scripts/batch_eval.sh` 中的 `sleep 5`。

### 如何添加新模型？

在OpenRouter支持的模型列表中选择，然后：

```bash
python -m backend.evaluator "MyModel" "provider/model-name"
```

### 结果如何解读？

- `raw_scores`: 各维度原始分数（2-6分）
- `levels`: L/M/H等级
- `pattern`: 15维度的模式字符串
- `sbiti_type`: 匹配的SBTI类型代码
- `chinese_name`: SBTI类型中文名
- `match_similarity`: 与标准类型的相似度百分比
- `exact_dimensions`: 精确匹配的维度数量

## 技术栈

- **后端**: Python 3.8+
- **API**: OpenRouter
- **前端**: 纯HTML/CSS/JavaScript
- **测试**: pytest
- **依赖管理**: pip

## 许可证

本项目基于原始SBTI测试项目改造。

## 致谢

- 原始SBTI测试：B站@蛆肉儿串儿
- 交互版开发：GitHub@sx349
