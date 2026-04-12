# SBTI-Bench: 大模型人格评测基准

<div align="center">

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Claude Code](https://img.shields.io/badge/Claude%20Code-AI%20Assisted-purple.svg)
![GitHub Stars](https://img.shields.io/github/stars/ybq22/SBTI-Bench?style=social)
![GitHub Issues](https://img.shields.io/github/issues/ybq22/SBTI-Bench)
![GitHub Contributors](https://img.shields.io/github/contributors/ybq22/SBTI-Bench)

**基于 SBTI 框架评估大语言模型人格特征的标准化基准**

</div>

---

## 🌟 关于

SBTI-Bench 是一个创新的基准测试项目，将真人 SBTI 性格测试系统改造成适用于大语言模型的评测工具。通过15个心理维度的标准化测试，我们评估不同 LLM 对性格相关问题的反应模式，从而洞察它们的行为倾向和决策模式。

### 🎯 项目意义

**理解 AI 人格**：随着 LLM 越来越多地融入日常生活，了解它们的"性格"特质变得至关重要：
- **负责任地部署 AI**：将模型特征与使用场景匹配
- **用户体验优化**：选择与应用基调一致的模型
- **安全性与可靠性**：识别潜在的有问题行为模式
- **对比分析**：客观比较不同模型系列和版本

**创新的基准测试方法**：不同于传统的性能基准测试，SBTI-Bench 探索了 AI 模型的*行为*和*心理*层面，为 AI 评估开辟了超越准确度和速度的新途径。

---

## ✨ 特性

- 🎭 **26种 SBTI 人格类型**：全面的性格分类系统
- 📊 **15维度分析**：跨5个心理模型的深入评估
  - 自我模型 (S1-S3)：自我认知与自信
  - 情感模型 (E1-E3)：情感安全与依恋
  - 态度模型 (A1-A3)：世界观与灵活性
  - 行动驱力模型 (Ac1-Ac3)：动机与决策
  - 社交模型 (So1-So3)：社交主动性与边界
- 🔌 **统一的 OpenRouter API**：通过单一接口支持100+种LLM模型
- 🚀 **批量评测**：高效测试多个模型
- 🎨 **精美前端**：支持明暗主题的交互式可视化
- 📈 **详细分析**：原始分数、等级、模式匹配和相似度指标

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/ybq22/SBTI-Bench.git
cd SBTI-Bench

# 安装依赖
pip install -r backend/requirements.txt
```

### 2. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 OpenRouter API 密钥
# OPENROUTER_API_KEY=你的实际API密钥
```

### 3. 运行评测

```bash
# 评测单个模型
python -m backend.evaluator "GPT-4" "openai/gpt-4"

# 批量评测
./batch_scripts/batch_eval.sh "openai/gpt-4" "anthropic/claude-3-opus" "meta-llama/llama-3-70b"
```

### 4. 查看结果

```bash
# 启动 HTTP 服务器
./start_server.sh

# 在浏览器中打开
# http://localhost:8001/frontend/index.html
```

---

## 📊 SBTI 人格类型

本基准将模型分为26种不同的人格类型：

### 常规类型（26种）

| 代码 | 名称 | 描述 | 模式 |
|------|------|------|------|
| CTRL | 拿捏者 | 天生的领导者，喜欢掌控和预见 | HHH-HMH-MHH-HHH-MHM |
| ATM-er | 送钱者 | 慷慨大方，资源丰富的性格 | HHH-HHM-HHH-HMH-MHL |
| Dior-s | 屌丝 | 自嘲但坚韧，逆境中的幽默 | MHM-MMH-MHM-HMH-LHL |
| BOSS | 领导者 | 果断的领导者，自然地掌舵 | HHH-HMH-MMH-HHH-LHL |
| THAN-K | 感恩者 | 对生活中的美好心存感激 | MHM-HMM-HHM-MMH-MHL |
| OH-NO | 哦不人 | 意外频发但能适应危机 | HHL-LMH-LHH-HHM-LHL |
| GOGO | 行者 | 行动导向，偏好执行胜过计划 | HHM-HMH-MMH-HHH-MHM |
| SEXY | 尤物 | 魅力四射，天生吸引力 | HMH-HHL-HMM-HMM-HLH |
| LOVE-R | 多情者 | 情感丰富，深情专一 | MLH-LHL-HLH-MLM-MLH |
| MUM | 妈妈 | 天生的照顾者，关心他人 | MMH-MHL-HMM-LMM-HLL |
| FAKE | 伪人 | 适应力强，层次复杂 | HLM-MML-MLM-MLM-HLH |
| OJBK | 无所谓人 | 超然物外，随遇而安 | MMH-MMM-HML-LMM-MML |
| MALO | 吗喽 | 在挣扎中寻找快乐 | MLH-MHM-MLH-MLH-LMH |
| JOKE-R | 小丑 | 用幽默掩饰内心敏感 | LLH-LHL-LML-LLL-MLM |
| WOC! | 握草人 | 情绪表达强烈且外放 | HHL-HMH-MMH-HHM-LHH |
| THIN-K | 思考者 | 深思熟虑，过度思考 | HHL-HMH-MLH-MHM-LHH |
| SHIT | 愤世者 | 批判性思维，看透表象 | HHL-HLH-LMM-HHM-LHH |
| ZZZZ | 装死者 | 通过回避避免冲突 | MHL-MLH-LML-MML-LHM |
| POOR | 贫困者 | 物质匮乏但精神丰富 | HHL-MLH-LMH-HHH-LHL |
| MONK | 僧人 | 超脱世俗欲望，追求平静 | HHL-LLH-LLM-MML-LHM |
| IMSB | 傻者 | 天真单纯，思维纯粹 | LLM-LMM-LLL-LLL-MLM |
| SOLO | 孤儿 | 独立自主，享受独处 | LML-LLH-LHL-LML-LHM |
| FUCK | 草者 | 直接真实，表达不加过滤 | MLL-LHL-LLM-MLL-HLH |
| DEAD | 死者 | 情感麻木，与生活脱节 | LLL-LLM-LML-LLL-LHM |
| IMFW | 废物 | 自我价值低但渴望认可 | LLH-LHL-LML-LLL-MLL |

### 特殊类型

| 代码 | 名称 | 触发条件 | 模式 |
|------|------|----------|------|
| DRUNK | 酒鬼 | 酒精相关门控问题触发 | 用户模式 |
| HHHH | 傻乐者 | 与所有常规类型相似度 <60% | HHH-HHH-HHH-HHH-HHH |

---

## 🧪 评测方法

### 1. 问题框架
- **30个问题**覆盖15个心理维度
- **多选答案**，加权计分（2-6分）
- **经过验证的心理构念**，适配AI评测

### 2. 计分系统
- **原始分数**：每个维度获得2-6分
- **等级转换**：分数映射为三个等级
  - **L (低)**：2-3分
  - **M (中)**：4分
  - **H (高)**：5-6分

### 3. 模式匹配
- **15维度模式**：L/M/H字符串（例如："HHH-HMH-MHH-HHH-MHM"）
- **曼哈顿距离算法**：找到最相似的人格类型
- **相似度分数**：百分比匹配度（0-100%）
- **精确维度数**：完全匹配的维度数量

### 4. 特殊情况
- **DRUNK 类型**：由特定酒精相关回答触发
- **HHHH 类型**：当没有常规类型超过60%相似度时的回退

---

## 📁 项目结构

```
SBTI-Bench/
├── backend/              # Python 后端
│   ├── questions.py     # SBTI 问题数据库
│   ├── scoring.py       # 计分逻辑
│   ├── matcher.py       # 人格匹配算法
│   ├── llm_interface.py # OpenRouter API 封装
│   └── evaluator.py     # 主评测脚本
├── batch_scripts/        # 批量评测脚本
│   └── batch_eval.sh    # 多模型评测
├── data/                # 评测数据
│   └── results.json     # 存储评测结果
├── frontend/            # 交互式前端
│   ├── index.html       # 主可视化页面
│   ├── diagnose.html    # 诊断工具
│   └── test.html        # 测试页面
├── image/               # 人格类型插图
│   ├── CTRL.png         # 类型插图（26种）
│   ├── BOSS.png
│   └── ...
├── tests/               # 单元测试
│   └── test_*.py       # 测试文件
├── docs/                # 文档
│   └── superpowers/   # 设计文档
└── README.md            # 本文件
```

---

## 📊 示例结果

热门模型的评测结果示例：

```json
{
  "model_name": "GPT-4",
  "sbiti_type": "CTRL",
  "chinese_name": "拿捏者",
  "match_similarity": 95,
  "pattern": "HHH-HMH-MHH-HHH-MHM"
}
```

---

## 🧪 开发

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行带覆盖率的测试
pytest tests/ -v --cov=backend

# 运行特定测试文件
pytest tests/test_evaluator.py -v
```

### 添加新模型

只需在批量评测脚本中添加模型：

```bash
./batch_scripts/batch_eval.sh \
  "你的模型名" \
  "provider/模型-id"
```

---

## 🤝 贡献

欢迎贡献！请随时提交 issue 或 pull request。

### 可贡献领域：
- 额外的模型评测
- 新的心理维度
- 改进的可视化
- 文档增强
- Bug修复和性能改进

---

## 📄 许可证

本项目基于原始 SBTI 测试项目改造，采用 MIT 许可证。

---

## 🙏 致谢

- **原始 SBTI 测试**：B站 @蛆肉儿串儿
- **交互版开发**：GitHub @sx349
- **OpenRouter**：统一访问多个 LLM 提供商

---

## 📞 联系方式

如有问题、建议或想法，请：
- 在 GitHub 上提交 issue
- 在 Discussions 标签中开始讨论

---

<div align="center">

**用 ❤️ 为 AI 社区打造**

**⭐ 如果觉得这个项目有用，请考虑给个星标！**

</div>

---

## 语言 / Language

[English](README_EN.md) | [简体中文](README.md)
