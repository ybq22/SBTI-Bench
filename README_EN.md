# SBTI-Bench: Large Model Personality Assessment Benchmark

<div align="center">

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Claude Code](https://img.shields.io/badge/Claude%20Code-AI%20Assisted-purple.svg)
![GitHub Stars](https://img.shields.io/github/stars/ybq22/SBTI-Bench?style=social)
![GitHub Issues](https://img.shields.io/github/issues/ybq22/SBTI-Bench)
![GitHub Contributors](https://img.shields.io/github/contributors/ybq22/SBTI-Bench)

**A standardized benchmark for evaluating personality characteristics of Large Language Models through SBTI framework**

</div>

---

## 🌟 About

SBTI-Bench is a novel benchmark that adapts the human SBTI personality test system to evaluate the "personality" traits of AI models. Through standardized testing across 15 psychological dimensions, we assess how different LLMs respond to personality-related questions, providing insights into their behavioral tendencies and decision-making patterns.

### 🎯 Why This Matters

**Understanding AI Personality**: As LLMs become more integrated into daily life, understanding their "personality" traits becomes crucial for:
- **Responsible AI Deployment**: Match model characteristics to use cases
- **User Experience Optimization**: Select models that align with application tone
- **Safety & Reliability**: Identify potentially problematic behavioral patterns
- **Comparative Analysis**: Objective comparison across model families and versions

**Novel Benchmarking Approach**: Unlike traditional performance benchmarks, SBTI-Bench explores the *behavioral* and *psychological* aspects of AI models, opening new avenues for AI evaluation beyond accuracy and speed.

---

## ✨ Features

- 🎭 **26 SBTI Personality Types**: Comprehensive personality classification system
- 📊 **15-Dimension Analysis**: In-depth evaluation across 5 psychological models
  - Self Model (S1-S3): Self-awareness and confidence
  - Emotion Model (E1-E3): Emotional security and attachment
  - Attitude Model (A1-A3): Worldview and flexibility
  - Action Drive Model (Ac1-Ac3): Motivation and decision-making
  - Social Model (So1-So3): Social initiative and boundaries
- 🔌 **Unified OpenRouter API**: Support for 100+ LLM models through single interface
- 🚀 **Batch Evaluation**: Efficient testing of multiple models
- 🎨 **Beautiful Frontend**: Interactive visualization with light/dark themes
- 📈 **Detailed Analytics**: Raw scores, levels, pattern matching, and similarity metrics

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/ybq22/SBTI-Bench.git
cd SBTI-Bench

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your OpenRouter API key
# OPENROUTER_API_KEY=your_actual_api_key_here
```

### 3. Run Evaluation

```bash
# Evaluate a single model
python -m backend.evaluator "GPT-4" "openai/gpt-4"

# Batch evaluation
./batch_scripts/batch_eval.sh "openai/gpt-4" "anthropic/claude-3-opus" "meta-llama/llama-3-70b"
```

### 4. View Results

```bash
# Start HTTP server
./start_server.sh

# Open in browser
# http://localhost:8001/frontend/index.html
```

---

## 📊 SBTI Personality Types

Our benchmark classifies models into 26 distinct personality types:

### Regular Types (26 Types)

| Code | Name | Description | Pattern |
|------|------|-------------|----------|
| CTRL | 掌控者 | Natural leaders who enjoy control and foresight | HHH-HMH-MHH-HHH-MHM |
| ATM-er | 送钱者 | Generous and giving, resource-rich personality | HHH-HHM-HHH-HMH-MHL |
| Dior-s | 屌丝 | Self-deprecating yet resilient humor in adversity | MHM-MMH-MHM-HMH-LHL |
| BOSS | 领导者 | Decisive leaders who take charge naturally | HHH-HMH-MMH-HHH-LHL |
| THAN-K | 感恩者 | Grateful and appreciative of life's goodness | MHM-HMM-HHM-MMH-MHL |
| OH-NO | 哦不人 | Accident-prone but adaptable to crises | HHL-LMH-LHH-HHM-LHL |
| GOGO | 行者 | Action-oriented doers who prefer execution over planning | HHM-HMH-MMH-HHH-MHM |
| SEXY | 尤物 | Charismatic and attractive with natural appeal | HMH-HHL-HMM-HMM-HLH |
| LOVE-R | 多情者 | Emotionally rich and deeply devoted in relationships | MLH-LHL-HLH-MLM-MLH |
| MUM | 妈妈 | Natural caregivers who look after others | MMH-MHL-HMM-LMM-HLL |
| FAKE | 伪人 | Adaptable with complex layers and hidden depths | HLM-MML-MLM-MLM-HLH |
| OJBK | 无所谓人 | Detached and accepting, goes with the flow | MMH-MMM-HML-LMM-MML |
| MALO | 吗喽 | Finds joy in self-deprecation amid life's struggles | MLH-MHM-MLH-MLH-LMH |
| JOKE-R | 小丑 | Uses humor to mask inner sensitivity and pain | LLH-LHL-LML-LLL-MLM |
| WOC! | 握草人 | Expressive and reactive with intense emotions | HHL-HMH-MMH-HHM-LHH |
| THIN-K | 思考者 | Thoughtful analysts who overthink decisions | HHL-HMH-MLH-MHM-LHH |
| SHIT | 愤世者 | Critical thinkers who see through facades | HHL-HLH-LMM-HHM-LHH |
| ZZZZ | 装死者 | Avoids confrontation through strategic avoidance | MHL-MLH-LML-MML-LHM |
| POOR | 贫困者 | Rich inner world despite material constraints | HHL-MLH-LMH-HHH-LHL |
| MONK | 僧人 | Detached from worldly desires, seeks peace | HHL-LLH-LLM-MML-LHM |
| IMSB | 傻者 | Innocently naive with pure, untainted thinking | LLM-LMM-LLL-LLL-MLM |
| SOLO | 孤儿 | Independent and self-reliant, comfortable alone | LML-LLH-LHL-LML-LHM |
| FUCK | 草者 | Direct and authentic, unfiltered expression | MLL-LHL-LLM-MLL-HLH |
| DEAD | 死者 | Emotionally numb and disengaged from life | LLL-LLM-LML-LLL-LHM |
| IMFW | 废物 | Low self-worth but渴望 recognition | LLH-LHL-LML-LLL-MLL |

### Special Types

| Code | Name | Trigger Condition | Pattern |
|------|------|------------------|---------|
| DRUNK | 酒鬼 | Alcohol-related gate question triggered | User's pattern |
| HHHH | 傻乐者 | Similarity < 60% with all regular types | HHH-HHH-HHH-HHH-HHH |

---

## 🧪 Evaluation Methodology

### 1. Question Framework
- **30 questions** covering 15 psychological dimensions
- **Multiple choice answers** with weighted scoring (2-6 points)
- **Validated psychological constructs** adapted for AI evaluation

### 2. Scoring System
- **Raw Scores**: Each dimension receives a score from 2-6 points
- **Level Conversion**: Scores map to three levels:
  - **L (Low)**: 2-3 points
  - **M (Medium)**: 4 points
  - **H (High)**: 5-6 points

### 3. Pattern Matching
- **15-Dimension Pattern**: L/M/H string (e.g., "HHH-HMH-MHH-HHH-MHM")
- **Manhattan Distance Algorithm**: Finds the most similar personality type
- **Similarity Score**: Percentage match (0-100%)
- **Exact Dimensions**: Count of perfectly matching dimensions

### 4. Special Cases
- **DRUNK Type**: Triggered by specific alcohol-related responses
- **HHHH Type**: Fallback when no regular type exceeds 60% similarity

---

## 📁 Project Structure

```
SBTI-Bench/
├── backend/              # Python backend
│   ├── questions.py     # SBTI question database
│   ├── scoring.py       # Scoring logic
│   ├── matcher.py       # Personality matching algorithm
│   ├── llm_interface.py # OpenRouter API wrapper
│   └── evaluator.py     # Main evaluation script
├── batch_scripts/        # Batch evaluation scripts
│   └── batch_eval.sh    # Multi-model evaluation
├── data/                # Evaluation data
│   └── results.json     # Stored evaluation results
├── frontend/            # Interactive frontend
│   ├── index.html       # Main visualization page
│   ├── diagnose.html    # Diagnostic tool
│   └── test.html        # Testing page
├── image/               # Personality type illustrations
│   ├── CTRL.png         # Type illustrations (26 types)
│   ├── BOSS.png
│   └── ...
├── tests/               # Unit tests
│   └── test_*.py       # Test files
├── docs/                # Documentation
│   └── superpowers/   # Design documentation
└── README.md            # This file
```

---

## 📊 Sample Results

Example evaluation results for popular models:

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

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=backend

# Run specific test file
pytest tests/test_evaluator.py -v
```

### Adding New Models

Simply add your model to the batch evaluation script:

```bash
./batch_scripts/batch_eval.sh \
  "your-model-name" \
  "provider/your-model-id"
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Areas for Contribution:
- Additional model evaluations
- New psychological dimensions
- Improved visualization
- Documentation enhancements
- Bug fixes and performance improvements

---

## 📄 License

This project is based on the original SBTI test and is released under the MIT License.

---

## 🙏 Acknowledgments

- **Original SBTI Test**: B站 @蛆肉儿串儿
- **Interactive Version**: GitHub @sx349
- **OpenRouter**: Unified API access to multiple LLM providers

---

## 📞 Contact

For questions, issues, or suggestions, please:
- Open an issue on GitHub
- Start a discussion in the Discussions tab

---

<div align="center">

**Made with ❤️ for the AI community**

**⭐ If you find this project useful, please consider giving it a star!**

</div>

---

## 语言 / Language

[English](README_EN.md) | [简体中文](README.md)
