# SBTI大模型评测系统实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-step. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个大模型SBTI评测基准系统，支持通过OpenRouter API评测多个AI模型的人格特征，并生成可视化对比报告

**Architecture:** Python后端负责数据提取、API调用、计分匹配；Bash脚本实现批量评测；HTML前端展示结果排行榜和类型分布

**Tech Stack:** Python 3.10+, requests, python-dotenv, OpenRouter API, Vanilla JS, Chart.js

---

## 文件结构

```
SBTI-Bench/
├── backend/                      # Python后端模块
│   ├── __init__.py              # 包初始化
│   ├── questions.py             # 从HTML提取问题数据
│   ├── scoring.py               # SBTI计分逻辑
│   ├── matcher.py               # 类型匹配算法
│   ├── llm_interface.py         # OpenRouter API接口
│   ├── evaluator.py             # 主评测脚本
│   └── requirements.txt         # Python依赖
├── batch_scripts/               # 批量评测脚本
│   └── batch_eval.sh            # Bash批量评测
├── data/                        # 评测数据存储
│   └── results.json             # 评测结果JSON
├── tests/                       # 单元测试
│   ├── test_questions.py
│   ├── test_scoring.py
│   ├── test_matcher.py
│   └── test_integration.py
├── .env.example                 # 环境变量模板
├── .env                         # 环境变量配置
└── README.md                    # 项目说明文档
```

---

## Task 1: 项目初始化和依赖配置

**Files:**
- Create: `backend/__init__.py`
- Create: `backend/requirements.txt`
- Create: `.env.example`
- Create: `data/.gitkeep`

- [ ] **Step 1: 创建Python包初始化文件**

```bash
mkdir -p backend batch_scripts data tests
touch backend/__init__.py data/.gitkeep
```

- [ ] **Step 2: 创建requirements.txt**

```python
# backend/requirements.txt
requests>=2.31.0
python-dotenv>=1.0.0
pytest>=7.4.0
```

- [ ] **Step 3: 创建环境变量模板**

```bash
# .env.example
OPENROUTER_API_KEY=your_api_key_here
DEFAULT_MODEL=openai/gpt-4
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000
```

- [ ] **Step 4: 创建.gitignore文件**

```bash
# .gitignore
.env
__pycache__/
*.pyc
.pytest_cache/
data/results.json
*.log
```

- [ ] **Step 5: 提交初始化文件**

```bash
git add backend/ batch_scripts/ data/ tests/ .env.example .gitignore
git commit -m "feat: initialize project structure and dependencies"
```

---

## Task 2: 从HTML提取问题数据

**Files:**
- Create: `backend/questions.py`
- Test: `tests/test_questions.py`

- [ ] **Step 1: 编写问题数据提取的测试**

```python
# tests/test_questions.py
import pytest
from backend.questions import get_dimension_meta, get_questions, get_special_questions, get_normal_types

def test_dimension_meta_structure():
    """验证维度元数据结构正确"""
    meta = get_dimension_meta()
    assert 'S1' in meta
    assert meta['S1']['name'] == 'S1 自尊自信'
    assert meta['S1']['model'] == '自我模型'

def test_questions_structure():
    """验证问题数据结构正确"""
    questions = get_questions()
    assert len(questions) == 30
    q1 = questions[0]
    assert q1['id'] == 'q1'
    assert q1['dim'] == 'S1'
    assert len(q1['options']) == 3
    assert 'text' in q1

def test_special_questions():
    """验证特殊问题存在"""
    special = get_special_questions()
    assert len(special) == 2
    assert special[0]['id'] == 'drink_gate_q1'
    assert special[1]['id'] == 'drink_gate_q2'

def test_normal_types_count():
    """验证常规类型数量正确"""
    types = get_normal_types()
    assert len(types) == 26
    ctrl_type = next(t for t in types if t['code'] == 'CTRL')
    assert ctrl_type['pattern'] == 'HHH-HMH-MHH-HHH-MHM'

def test_reverse_scoring_question():
    """验证q27是反向计分问题"""
    questions = get_questions()
    q27 = next(q for q in questions if q['id'] == 'q27')
    assert q27['dim'] == 'So2'
    assert '电子围栏' in q27['text']
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd /Users/yuebaoqing/Desktop/projects/SBTI-Bench
pytest tests/test_questions.py -v
```

Expected: FAIL - ModuleNotFoundError: No module named 'backend.questions'

- [ ] **Step 3: 实现questions.py模块**

```python
# backend/questions.py
"""
从现有index.html提取SBTI测试数据
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Any

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
HTML_FILE = PROJECT_ROOT / "index.html"


def extract_javascript_data(html_content: str) -> Dict[str, Any]:
    """
    从HTML文件中提取JavaScript数据结构
    """
    # 提取dimensionMeta
    dimension_meta_match = re.search(
        r'const dimensionMeta = (\{.*?\});',
        html_content,
        re.DOTALL
    )

    # 提取questions数组
    questions_match = re.search(
        r'const questions = (\[.*?\]);',
        html_content,
        re.DOTALL
    )

    # 提取specialQuestions数组
    special_questions_match = re.search(
        r'const specialQuestions = (\[.*?\]);',
        html_content,
        re.DOTALL
    )

    # 提取NORMAL_TYPES数组
    normal_types_match = re.search(
        r'const NORMAL_TYPES = (\[.*?\]);',
        html_content,
        re.DOTALL
    )

    # 提取DIM_EXPLANATIONS对象
    dim_explanations_match = re.search(
        r'const DIM_EXPLANATIONS = (\{.*?\});',
        html_content,
        re.DOTALL
    )

    data = {}

    if dimension_meta_match:
        data['dimensionMeta'] = json.loads(dimension_meta_match.group(1))
    if questions_match:
        data['questions'] = json.loads(questions_match.group(1))
    if special_questions_match:
        data['specialQuestions'] = json.loads(special_questions_match.group(1))
    if normal_types_match:
        data['normalTypes'] = json.loads(normal_types_match.group(1))
    if dim_explanations_match:
        data['dimExplanations'] = json.loads(dim_explanations_match.group(1))

    return data


def get_dimension_meta() -> Dict[str, Dict[str, str]]:
    """获取维度元数据"""
    html_content = HTML_FILE.read_text(encoding='utf-8')
    data = extract_javascript_data(html_content)
    return data.get('dimensionMeta', {})


def get_questions() -> List[Dict[str, Any]]:
    """获取30个常规问题"""
    html_content = HTML_FILE.read_text(encoding='utf-8')
    data = extract_javascript_data(html_content)
    return data.get('questions', [])


def get_special_questions() -> List[Dict[str, Any]]:
    """获取2个特殊问题（酒鬼触发）"""
    html_content = HTML_FILE.read_text(encoding='utf-8')
    data = extract_javascript_data(html_content)
    return data.get('specialQuestions', [])


def get_normal_types() -> List[Dict[str, str]]:
    """获取26种常规SBTI类型"""
    html_content = HTML_FILE.read_text(encoding='utf-8')
    data = extract_javascript_data(html_content)
    return data.get('normalTypes', [])


def get_dim_explanations() -> Dict[str, Dict[str, str]]:
    """获取各维度L/M/H等级解释"""
    html_content = HTML_FILE.read_text(encoding='utf-8')
    data = extract_javascript_data(html_content)
    return data.get('dimExplanations', {})


def get_all_data() -> Dict[str, Any]:
    """获取所有数据"""
    html_content = HTML_FILE.read_text(encoding='utf-8')
    return extract_javascript_data(html_content)
```

- [ ] **Step 4: 运行测试验证通过**

```bash
pytest tests/test_questions.py -v
```

Expected: PASS (所有测试通过)

- [ ] **Step 5: 提交代码**

```bash
git add backend/questions.py tests/test_questions.py
git commit -m "feat: implement question data extraction from HTML"
```

---

## Task 3: 实现SBTI计分逻辑

**Files:**
- Create: `backend/scoring.py`
- Test: `tests/test_scoring.py`

- [ ] **Step 1: 编写计分逻辑测试**

```python
# tests/test_scoring.py
import pytest
from backend.scoring import calculate_scores, scores_to_levels, generate_pattern

def test_calculate_scores_all_a():
    """测试全部选择A选项(1分)的计分"""
    answers = {f'q{i}': 1 for i in range(1, 31)}
    scores = calculate_scores(answers)

    # 大部分维度应该是低分
    assert scores['S1'] <= 3  # L
    assert scores['E1'] <= 3  # L

def test_calculate_scores_all_c():
    """测试全部选择C选项(3分)的计分"""
    answers = {f'q{i}': 3 for i in range(1, 31)}
    scores = calculate_scores(answers)

    # 大部分维度应该是高分
    assert scores['S1'] >= 5  # H
    assert scores['E1'] >= 5  # H

def test_calculate_scores_with_reverse_scoring():
    """测试q27反向计分"""
    answers = {f'q{i}': 1 for i in range(1, 31)}  # 全部选择1
    answers['q27'] = 1  # q27选择1，反向计分应该+1分
    scores = calculate_scores(answers)

    # q27影响So2维度，应该比其他维度高
    assert scores['So2'] > scores['S1']

def test_scores_to_levels():
    """测试分数转等级"""
    assert scores_to_levels(2) == 'L'
    assert scores_to_levels(3) == 'L'
    assert scores_to_levels(4) == 'M'
    assert scores_to_levels(5) == 'H'
    assert scores_to_levels(6) == 'H'

def test_generate_pattern():
    """测试生成模式字符串"""
    levels = {
        'S1': 'H', 'S2': 'M', 'S3': 'H',
        'E1': 'L', 'E2': 'M', 'E3': 'H',
        'A1': 'M', 'A2': 'M', 'A3': 'H',
        'Ac1': 'H', 'Ac2': 'M', 'Ac3': 'H',
        'So1': 'M', 'So2': 'M', 'So3': 'L'
    }
    pattern = generate_pattern(levels)
    assert pattern == 'HMH-HMH-HMM-MMH-MHM'

def test_full_scoring_workflow():
    """测试完整计分流程"""
    # 构造一个应该匹配CTRL类型的答案
    answers = {
        'q1': 3, 'q2': 3,  # S1: H
        'q3': 2, 'q4': 2,  # S2: M
        'q5': 3, 'q6': 3,  # S3: H
        'q7': 2, 'q8': 1,  # E1: L
        'q9': 3, 'q10': 2, # E2: M
        'q11': 3, 'q12': 3, # E3: H
        'q13': 2, 'q14': 2, # A1: M
        'q15': 2, 'q16': 2, # A2: M
        'q17': 3, 'q18': 3, # A3: H
        'q19': 3, 'q20': 3, # Ac1: H
        'q21': 2, 'q22': 3, # Ac2: M
        'q23': 3, 'q24': 3, # Ac3: H
        'q25': 2, 'q26': 2, # So1: M
        'q27': 2, 'q28': 2, # So2: M (q27反向计分)
        'q29': 1, 'q30': 1, # So3: L
    }

    scores = calculate_scores(answers)
    levels = scores_to_levels_dict(scores)
    pattern = generate_pattern(levels)

    assert pattern == 'HMH-HMH-HMM-MMH-MHM'
```

- [ ] **Step 2: 运行测试验证失败**

```bash
pytest tests/test_scoring.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现scoring.py模块**

```python
# backend/scoring.py
"""
SBTI计分逻辑实现
"""
from typing import Dict

# 维度顺序（与原HTML一致）
DIMENSION_ORDER = ['S1','S2','S3','E1','E2','E3','A1','A2','A3','Ac1','Ac2','Ac3','So1','So2','So3']

# 问题到维度的映射
QUESTION_DIMENSIONS = {
    'q1': 'S1', 'q2': 'S1',
    'q3': 'S2', 'q4': 'S2',
    'q5': 'S3', 'q6': 'S3',
    'q7': 'E1', 'q8': 'E1',
    'q9': 'E2', 'q10': 'E2',
    'q11': 'E3', 'q12': 'E3',
    'q13': 'A1', 'q14': 'A1',
    'q15': 'A2', 'q16': 'A2',
    'q17': 'A3', 'q18': 'A3',
    'q19': 'Ac1', 'q20': 'Ac1',
    'q21': 'Ac2', 'q22': 'Ac2',
    'q23': 'Ac3', 'q24': 'Ac3',
    'q25': 'So1', 'q26': 'So1',
    'q27': 'So2', 'q28': 'So2',
    'q29': 'So3', 'q30': 'So3'
}

# 反向计分问题
REVERSE_SCORING_QUESTIONS = {'q27'}


def calculate_scores(answers: Dict[str, int]) -> Dict[str, int]:
    """
    根据答案计算各维度原始分数

    Args:
        answers: 问题答案字典 {question_id: answer_value}

    Returns:
        各维度原始分数字典 {dimension: score}
    """
    # 初始化分数：每个维度从4分开始（2个问题×默认2分）
    scores = {dim: 4 for dim in DIMENSION_ORDER}

    # 根据答案调整分数
    for q_id, answer_value in answers.items():
        if q_id not in QUESTION_DIMENSIONS:
            continue

        dimension = QUESTION_DIMENSIONS[q_id]

        # q27反向计分
        if q_id in REVERSE_SCORING_QUESTIONS:
            # value 1→+1分, 2→0分, 3→-1分
            delta = 2 - answer_value
        else:
            # 正常计分: value 1→-1分, 2→0分, 3→+1分
            delta = answer_value - 2

        scores[dimension] += delta

    return scores


def scores_to_levels(score: int) -> str:
    """
    将分数转换为L/M/H等级

    Args:
        score: 原始分数

    Returns:
        等级 ('L', 'M', 'H')
    """
    if score <= 3:
        return 'L'
    elif score == 4:
        return 'M'
    else:
        return 'H'


def scores_to_levels_dict(scores: Dict[str, int]) -> Dict[str, str]:
    """
    将分数字典转换为等级字典

    Args:
        scores: 各维度原始分数

    Returns:
        各维度等级字典
    """
    return {dim: scores_to_levels(score) for dim, score in scores.items()}


def generate_pattern(levels: Dict[str, str]) -> str:
    """
    生成SBTI模式字符串

    Args:
        levels: 各维度等级字典

    Returns:
        模式字符串，如 "HMH-HMH-HMM-MMH-MHM"
    """
    pattern_parts = []
    for i, dim in enumerate(DIMENSION_ORDER):
        pattern_parts.append(levels[dim])
        # 每5个维度添加一个分隔符
        if (i + 1) % 5 == 0 and i < len(DIMENSION_ORDER) - 1:
            pattern_parts.append('-')

    return ''.join(pattern_parts)
```

- [ ] **Step 4: 运行测试验证通过**

```bash
pytest tests/test_scoring.py -v
```

Expected: PASS

- [ ] **Step 5: 提交代码**

```bash
git add backend/scoring.py tests/test_scoring.py
git commit -m "feat: implement SBTI scoring logic with reverse scoring support"
```

---

## Task 4: 实现类型匹配算法

**Files:**
- Create: `backend/matcher.py`
- Test: `tests/test_matcher.py`

- [ ] **Step 1: 编写匹配算法测试**

```python
# tests/test_matcher.py
import pytest
from backend.matcher import find_best_match, calculate_similarity, level_to_num

def test_level_to_num():
    """测试等级转数值"""
    assert level_to_num('L') == 1
    assert level_to_num('M') == 2
    assert level_to_num('H') == 3

def test_calculate_similarity():
    """测试相似度计算"""
    # 完全匹配
    user_pattern = "HHH-HMH-MHH-HHH-MHM"
    type_pattern = "HHH-HMH-MHH-HHH-MHM"
    similarity = calculate_similarity(user_pattern, type_pattern)
    assert similarity == 100

    # 完全不匹配
    user_pattern = "LLL-LLL-LLL-LLL-LLL"
    type_pattern = "HHH-HHH-HHH-HHH-HHH"
    similarity = calculate_similarity(user_pattern, type_pattern)
    assert similarity < 50

def test_find_best_match_ctrl():
    """测试匹配CTRL类型"""
    user_pattern = "HHH-HMH-MHH-HHH-MHM"
    result = find_best_match(user_pattern)

    assert result['code'] == 'CTRL'
    assert result['similarity'] == 100

def test_find_best_match_with_drunk_trigger():
    """测试酒鬼触发"""
    user_pattern = "HHH-HMH-MHH-HHH-MHM"
    drunk_triggered = True
    result = find_best_match(user_pattern, drunk_triggered=drunk_triggered)

    assert result['code'] == 'DRUNK'
    assert result['similarity'] == 100

def test_find_best_match_hhhh_fallback():
    """测试HHHH兜底"""
    user_pattern = "LML-LML-LML-LML-LML"  # 极低相似度
    result = find_best_match(user_pattern, drunk_triggered=False)

    # 如果最佳匹配度<60%，应该返回HHHH
    assert result['similarity'] < 60
    # 但常规匹配应该仍然返回最佳类型
    # HHHH触发应该在evaluator层面处理

def test_find_best_match_ranking():
    """测试匹配排序"""
    user_pattern = "HHH-HMH-MHH-HHH-MHM"
    ranked = find_best_match(user_pattern, return_all=True)

    assert len(ranked) == 26
    # CTRL应该是第一名
    assert ranked[0]['code'] == 'CTRL'
    assert ranked[0]['similarity'] == 100
```

- [ ] **Step 2: 运行测试验证失败**

```bash
pytest tests/test_matcher.py -v
```

Expected: FAIL

- [ ] **Step 3: 实现matcher.py模块**

```python
# backend/matcher.py
"""
SBTI类型匹配算法
"""
from typing import List, Dict, Any, Optional
from backend.questions import get_normal_types, get_dim_explanations

# 类型库缓存
_NORMAL_TYPES = None
_DIM_EXPLANATIONS = None


def _get_normal_types() -> List[Dict[str, str]]:
    """获取常规类型（带缓存）"""
    global _NORMAL_TYPES
    if _NORMAL_TYPES is None:
        _NORMAL_TYPES = get_normal_types()
    return _NORMAL_TYPES


def level_to_num(level: str) -> int:
    """将L/M/H转换为数值"""
    return {'L': 1, 'M': 2, 'H': 3}[level]


def parse_pattern(pattern: str) -> List[int]:
    """将模式字符串转换为数值列表"""
    return [level_to_num(c) for c in pattern.replace('-', '')]


def calculate_similarity(user_pattern: str, type_pattern: str) -> int:
    """
    计算用户模式与类型模式的相似度

    Args:
        user_pattern: 用户模式字符串
        type_pattern: 类型模式字符串

    Returns:
        相似度百分比 (0-100)
    """
    user_vector = parse_pattern(user_pattern)
    type_vector = parse_pattern(type_pattern)

    # 计算曼哈顿距离
    distance = sum(abs(u - t) for u, t in zip(user_vector, type_vector))

    # 转换为相似度（最大距离30）
    similarity = max(0, round((1 - distance / 30) * 100))
    return similarity


def count_exact_matches(user_pattern: str, type_pattern: str) -> int:
    """计算精确匹配的维度数量"""
    user_vector = parse_pattern(user_pattern)
    type_vector = parse_pattern(type_pattern)
    return sum(1 for u, t in zip(user_vector, type_vector) if u == t)


def find_best_match(
    user_pattern: str,
    drunk_triggered: bool = False,
    return_all: bool = False
) -> Any:
    """
    查找最佳匹配的SBTI类型

    Args:
        user_pattern: 用户模式字符串
        drunk_triggered: 是否触发酒鬼类型
        return_all: 是否返回所有排序结果

    Returns:
        最佳匹配类型信息或排序后的类型列表
    """
    normal_types = _get_normal_types()

    # 计算所有类型的匹配度
    ranked = []
    for type_info in normal_types:
        type_pattern = type_info['pattern']
        distance = 0
        exact = 0

        user_vector = parse_pattern(user_pattern)
        type_vector = parse_pattern(type_pattern)

        for i in range(len(user_vector)):
            diff = abs(user_vector[i] - type_vector[i])
            distance += diff
            if diff == 0:
                exact += 1

        similarity = max(0, round((1 - distance / 30) * 100))

        ranked.append({
            'code': type_info['code'],
            'pattern': type_pattern,
            'distance': distance,
            'exact': exact,
            'similarity': similarity
        })

    # 排序：距离升序，精确匹配降序，相似度降序
    ranked.sort(key=lambda x: (x['distance'], -x['exact'], -x['similarity']))

    if return_all:
        return ranked

    # 处理特殊类型
    if drunk_triggered:
        return {
            'code': 'DRUNK',
            'chinese_name': '酒鬼',
            'pattern': user_pattern,
            'similarity': 100,
            'exact': 15,
            'special': True,
            'best_normal': ranked[0] if ranked else None
        }

    best = ranked[0]
    return {
        'code': best['code'],
        'pattern': best['pattern'],
        'similarity': best['similarity'],
        'exact': best['exact'],
        'special': False
    }


def should_trigger_hhhh(best_similarity: int) -> bool:
    """
    判断是否应该触发HHHH兜底类型

    Args:
        best_similarity: 最佳匹配相似度

    Returns:
        是否触发HHHH
    """
    return best_similarity < 60
```

- [ ] **Step 4: 运行测试验证通过**

```bash
pytest tests/test_matcher.py -v
```

Expected: PASS

- [ ] **Step 5: 提交代码**

```bash
git add backend/matcher.py tests/test_matcher.py
git commit -m "feat: implement SBTI type matching algorithm"
```

---

## Task 5: 实现OpenRouter API接口

**Files:**
- Create: `backend/llm_interface.py`
- Create: `.env` (从.env.example复制)
- Test: `tests/test_llm_interface.py`

- [ ] **Step 1: 编写API接口测试**

```python
# tests/test_llm_interface.py
import pytest
from unittest.mock import patch, MagicMock
from backend.llm_interface import LLMInterface, parse_answer

def test_parse_answer_simple():
    """测试解析简单字母答案"""
    assert parse_answer("A") == 1
    assert parse_answer("B") == 2
    assert parse_answer("C") == 3
    assert parse_answer("D") == 4

def test_parse_answer_with_text():
    """测试解析包含文字的答案"""
    assert parse_answer("我选择A") == 1
    assert parse_answer("答案是B") == 2
    assert parse_answer("选C") == 3

def test_parse_answer_lowercase():
    """测试解析小写字母"""
    assert parse_answer("a") == 1
    assert parse_answer("b") == 2
    assert parse_answer("c") == 3

def test_parse_answer_invalid():
    """测试解析无效答案"""
    assert parse_answer("我不知道") == 2  # 默认返回M
    assert parse_answer("") == 2
    assert parse_answer("E") == 2  # 超出范围

def test_llm_interface_init():
    """测试LLM接口初始化"""
    interface = LLMInterface(api_key="test_key")
    assert interface.api_key == "test_key"
    assert interface.model == "openai/gpt-4"

@patch('backend.llm_interface.requests.post')
def test_call_model_success(mock_post):
    """测试成功调用模型"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [{
            'message': {
                'content': 'A'
            }
        }]
    }
    mock_post.return_value = mock_response

    interface = LLMInterface(api_key="test_key")
    result = interface.call_model("test prompt")

    assert result == 'A'

def test_call_model_with_retry(mock_post):
    """测试API调用重试机制"""
    # 第一次失败，第二次成功
    mock_post.side_effect = [
        MagicMock(status_code=429),  # 限流
        MagicMock(status_code=200, json=lambda: {'choices': [{'message': {'content': 'B'}}]})
    ]

    interface = LLMInterface(api_key="test_key", max_retries=2)
    result = interface.call_model("test prompt")

    assert result == 'B'
    assert mock_post.call_count == 2
```

- [ ] **Step 2: 运行测试验证失败**

```bash
pytest tests/test_llm_interface.py -v
```

Expected: FAIL

- [ ] **Step 3: 实现llm_interface.py模块**

```python
# backend/llm_interface.py
"""
OpenRouter API接口
"""
import os
import re
import time
import requests
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def parse_answer(response_text: str) -> int:
    """
    解析模型回答，提取选项值

    Args:
        response_text: 模型的原始回答

    Returns:
        选项值 (1-4)
    """
    text = response_text.strip()

    # 尝试提取大写字母A-D
    match = re.search(r'[A-D]', text.upper())
    if match:
        letter = match.group(0)
        return ord(letter) - ord('A') + 1

    # 尝试提取小写字母a-d
    match = re.search(r'[a-d]', text)
    if match:
        letter = match.group(0)
        return ord(letter) - ord('a') + 1

    # 无法解析，返回默认值2（M）
    return 2


class LLMInterface:
    """大语言模型接口"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        初始化LLM接口

        Args:
            api_key: OpenRouter API密钥
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.model = model or os.getenv('DEFAULT_MODEL', 'openai/gpt-4')
        self.temperature = temperature or float(os.getenv('DEFAULT_TEMPERATURE', 0.7))
        self.max_tokens = max_tokens or int(os.getenv('DEFAULT_MAX_TOKENS', 1000))
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is required")

    def call_model(self, prompt: str) -> str:
        """
        调用大语言模型

        Args:
            prompt: 提示词

        Returns:
            模型回答
        """
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=30
                )

                # 处理限流
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (2 ** attempt))
                        continue
                    else:
                        raise Exception("Rate limit exceeded")

                response.raise_for_status()
                result = response.json()

                # 提取回答
                content = result['choices'][0]['message']['content']
                return content.strip()

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise Exception("Request timeout")

            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise Exception(f"API call failed: {str(e)}")

        raise Exception("Max retries exceeded")

    def evaluate_question(self, question_text: str, options: list) -> int:
        """
        让模型回答一个问题

        Args:
            question_text: 问题文本
            options: 选项列表

        Returns:
            选择的选项值 (1-4)
        """
        # 构建提示词
        prompt = self._build_prompt(question_text, options)

        # 调用模型
        response = self.call_model(prompt)

        # 解析回答
        answer = parse_answer(response)

        return answer

    def _build_prompt(self, question_text: str, options: list) -> str:
        """构建提示词"""
        options_text = "\n".join([
            f"{chr(ord('A') + i)}. {opt['label']}"
            for i, opt in enumerate(options)
        ])

        prompt = f"""你正在参与一个关于自我认知、情感、态度、行动和社交倾向的心理测试。
请根据你的真实倾向选择最符合的答案。

{question_text}

{options_text}

对于这个问题，请只回答选项字母（A/B/C/D），不要添加其他解释。"""

        return prompt
```

- [ ] **Step 4: 创建.env文件**

```bash
cp .env.example .env
# 编辑.env，添加真实的API密钥
```

- [ ] **Step 5: 运行测试验证通过**

```bash
pytest tests/test_llm_interface.py -v
```

Expected: PASS

- [ ] **Step 6: 提交代码**

```bash
git add backend/llm_interface.py .env.example tests/test_llm_interface.py
git commit -m "feat: implement OpenRouter API interface with retry logic"
```

---

## Task 6: 实现主评测脚本

**Files:**
- Create: `backend/evaluator.py`
- Test: `tests/test_evaluator.py`

- [ ] **Step 1: 编写评测脚本测试**

```python
# tests/test_evaluator.py
import pytest
from unittest.mock import patch, MagicMock
from backend.evaluator import SBTEEvaluator
import json

def test_evaluator_init():
    """测试评测器初始化"""
    evaluator = SBTEEvaluator(model_name="test-model")
    assert evaluator.model_name == "test-model"

@patch('backend.evaluator.LLMInterface')
def test_evaluate_single_question(mock_llm):
    """测试评测单个问题"""
    mock_llm.return_value.evaluate_question.return_value = 2

    evaluator = SBTEEvaluator(model_name="test-model")
    question = {
        'id': 'q1',
        'dim': 'S1',
        'text': '测试问题',
        'options': [
            {'label': '选项A', 'value': 1},
            {'label': '选项B', 'value': 2},
            {'label': '选项C', 'value': 3}
        ]
    }

    answer = evaluator.evaluate_question(question)
    assert answer == 2

def test_compute_result():
    """测试计算评测结果"""
    evaluator = SBTEEvaluator(model_name="test-model")

    answers = {
        'q1': 3, 'q2': 3, 'q3': 2, 'q4': 2, 'q5': 3, 'q6': 3,
        'q7': 2, 'q8': 1, 'q9': 3, 'q10': 2, 'q11': 3, 'q12': 3,
        'q13': 2, 'q14': 2, 'q15': 2, 'q16': 2, 'q17': 3, 'q18': 3,
        'q19': 3, 'q20': 3, 'q21': 2, 'q22': 3, 'q23': 3, 'q24': 3,
        'q25': 2, 'q26': 2, 'q27': 2, 'q28': 2, 'q29': 1, 'q30': 1
    }

    result = evaluator.compute_result(answers)

    assert 'raw_scores' in result
    assert 'levels' in result
    assert 'pattern' in result
    assert 'sbiti_type' in result
    assert result['model_name'] == "test-model"

def test_save_result():
    """测试保存评测结果"""
    evaluator = SBTEEvaluator(model_name="test-model")
    result = {
        'model_name': 'test-model',
        'sbiti_type': 'CTRL',
        'pattern': 'HHH-HMH-MHH-HHH-MHM'
    }

    evaluator.save_result(result, output_file='data/test_results.json')

    # 验证文件存在
    import os
    assert os.path.exists('data/test_results.json')

    # 验证内容
    with open('data/test_results.json', 'r') as f:
        data = json.load(f)
        assert data['model_name'] == 'test-model'

    # 清理
    os.remove('data/test_results.json')
```

- [ ] **Step 2: 运行测试验证失败**

```bash
pytest tests/test_evaluator.py -v
```

Expected: FAIL

- [ ] **Step 3: 实现evaluator.py模块**

```python
# backend/evaluator.py
"""
SBTI评测主脚本
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from backend.questions import get_questions, get_special_questions
from backend.scoring import calculate_scores, scores_to_levels_dict, generate_pattern
from backend.matcher import find_best_match, should_trigger_hhhh
from backend.llm_interface import LLMInterface


class SBTEEvaluator:
    """SBTI评测器"""

    def __init__(
        self,
        model_name: str,
        model_id: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        初始化评测器

        Args:
            model_name: 模型显示名称
            model_id: OpenRouter模型ID（如openai/gpt-4）
            api_key: OpenRouter API密钥
        """
        self.model_name = model_name
        self.model_id = model_id or model_name
        self.llm = LLMInterface(api_key=api_key)
        self.llm.model = self.model_id

        self.questions = get_questions()
        self.special_questions = get_special_questions()
        self.all_answers = {}

    def evaluate_question(self, question: Dict[str, Any]) -> int:
        """
        评测单个问题

        Args:
            question: 问题数据

        Returns:
            选择的选项值
        """
        answer = self.llm.evaluate_question(
            question['text'],
            question['options']
        )
        return answer

    def evaluate_all_questions(self) -> Dict[str, int]:
        """
        评测所有问题

        Returns:
            所有问题的答案字典
        """
        print(f"开始评测模型: {self.model_name}")
        print(f"使用模型ID: {self.model_id}")
        print("-" * 50)

        # 评测常规问题
        for i, question in enumerate(self.questions, 1):
            print(f"正在回答问题 {i}/{len(self.questions)}: {question['id']}")
            answer = self.evaluate_question(question)
            self.all_answers[question['id']] = answer
            print(f"  答案: {answer}")

        # 检查是否需要回答特殊问题
        q1_answer = self.all_answers.get('drink_gate_q1')
        if q1_answer == 3:  # 选择了"饮酒"
            # 询问第二个特殊问题
            q2 = self.special_questions[1]
            print(f"正在回答特殊问题: {q2['id']}")
            answer = self.evaluate_question(q2)
            self.all_answers[q2['id']] = answer
            print(f"  答案: {answer}")

        print("-" * 50)
        print("评测完成！")

        return self.all_answers

    def compute_result(self, answers: Dict[str, int]) -> Dict[str, Any]:
        """
        计算评测结果

        Args:
            answers: 问题答案字典

        Returns:
            评测结果字典
        """
        # 计算原始分数
        raw_scores = calculate_scores(answers)

        # 转换为等级
        levels = scores_to_levels_dict(raw_scores)

        # 生成模式字符串
        pattern = generate_pattern(levels)

        # 检查酒鬼触发
        drunk_triggered = (
            answers.get('drink_gate_q1') == 3 and
            answers.get('drink_gate_q2') == 2
        )

        # 查找最佳匹配
        match_result = find_best_match(pattern, drunk_triggered=drunk_triggered)

        # 检查HHHH触发
        if not drunk_triggered and should_trigger_hhhh(match_result['similarity']):
            sbiti_type = 'HHHH'
            chinese_name = '傻乐者'
            is_special = True
        else:
            sbiti_type = match_result['code']
            # 从类型库获取中文名称
            from backend.questions import get_all_data
            all_data = get_all_data()
            type_library = all_data.get('TYPE_LIBRARY', {})
            chinese_name = type_library.get(sbiti_type, {}).get('cn', sbiti_type)
            is_special = match_result.get('special', False)

        return {
            'model_name': self.model_name,
            'model_id': self.model_id,
            'evaluation_date': datetime.now().isoformat(),
            'raw_scores': raw_scores,
            'levels': levels,
            'pattern': pattern,
            'sbiti_type': sbiti_type,
            'chinese_name': chinese_name,
            'match_similarity': match_result['similarity'],
            'exact_dimensions': match_result['exact'],
            'is_special': is_special,
            'drunk_triggered': drunk_triggered,
            'answers': answers,
            'api_params': {
                'model': self.model_id,
                'temperature': self.llm.temperature,
                'max_tokens': self.llm.max_tokens
            }
        }

    def save_result(
        self,
        result: Dict[str, Any],
        output_file: str = 'data/results.json'
    ):
        """
        保存评测结果

        Args:
            result: 评测结果字典
            output_file: 输出文件路径
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 读取现有结果
        existing_results = []
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    existing_results = data.get('evaluations', [])
                except json.JSONDecodeError:
                    pass

        # 添加新结果
        existing_results.append(result)

        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'total_evaluations': len(existing_results),
                'evaluations': existing_results
            }, f, indent=2, ensure_ascii=False)

        print(f"结果已保存到: {output_file}")

    def run(self, output_file: str = 'data/results.json') -> Dict[str, Any]:
        """
        运行完整评测流程

        Args:
            output_file: 输出文件路径

        Returns:
            评测结果字典
        """
        # 评测所有问题
        answers = self.evaluate_all_questions()

        # 计算结果
        result = self.compute_result(answers)

        # 保存结果
        self.save_result(result, output_file)

        return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python -m backend.evaluator <model_name> [model_id]")
        sys.exit(1)

    model_name = sys.argv[1]
    model_id = sys.argv[2] if len(sys.argv) > 2 else None

    evaluator = SBTEEvaluator(model_name, model_id)
    result = evaluator.run()

    print("\n" + "=" * 50)
    print("评测结果:")
    print(f"模型: {result['model_name']}")
    print(f"SBTI类型: {result['sbiti_type']} ({result['chinese_name']})")
    print(f"匹配度: {result['match_similarity']}%")
    print(f"模式: {result['pattern']}")
    print("=" * 50)


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: 运行测试验证通过**

```bash
pytest tests/test_evaluator.py -v
```

Expected: PASS

- [ ] **Step 5: 提交代码**

```bash
git add backend/evaluator.py tests/test_evaluator.py backend/__init__.py
git commit -m "feat: implement main SBTI evaluation script"
```

---

## Task 7: 创建批量评测脚本

**Files:**
- Create: `batch_scripts/batch_eval.sh`
- Modify: `batch_scripts/batch_eval.sh`

- [ ] **Step 1: 创建批量评测脚本**

```bash
# batch_scripts/batch_eval.sh
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
```

- [ ] **Step 2: 添加执行权限**

```bash
chmod +x batch_scripts/batch_eval.sh
```

- [ ] **Step 3: 提交脚本**

```bash
git add batch_scripts/batch_eval.sh
git commit -m "feat: add batch evaluation script"
```

---

## Task 8: 创建项目文档

**Files:**
- Create: `README.md`
- Modify: `README.md`

- [ ] **Step 1: 创建README文档**

```markdown
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

## 项目结构

```
SBTI-Bench/
├── backend/              # Python后端
├── batch_scripts/        # 批量脚本
├── data/                # 评测数据
├── image/               # SBTI类型图片
├── index.html           # 原始测试页面
└── README.md            # 项目文档
```

## SBTI类型

本系统支持26种SBTI人格类型：

- CTRL (拿捏者), BOSS (领导者), SHIT (愤世者)
- DRUNK (酒鬼), HHHH (傻乐者), 以及其他21种类型

## 评测原理

1. **30个问题**覆盖15个维度
2. **维度评分**转换为L/M/H三个等级
3. **向量匹配**算法找到最相似的SBTI类型
4. **特殊类型**触发机制（酒鬼、傻乐者）

## 结果展示

评测结果保存在 `data/results.json`，包含：

- 模型名称和ID
- SBTI类型和中文名称
- 15个维度的原始分数和等级
- 匹配度和模式字符串
- 详细的问题回答

## 开发

运行测试：

```bash
pytest tests/ -v
```

## 许可证

本项目基于原始SBTI测试项目改造。

## 致谢

- 原始SBTI测试：B站@蛆肉儿串儿
- 交互版开发：GitHub@sx349
```

- [ ] **Step 2: 提交文档**

```bash
git add README.md
git commit -m "docs: add comprehensive README documentation"
```

---

## Task 9: 运行集成测试

**Files:**
- Create: `tests/test_integration.py`
- Test: `tests/test_integration.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/test_integration.py
import pytest
import json
from pathlib import Path
from backend.evaluator import SBTEEvaluator
from backend.questions import get_questions
from backend.scoring import calculate_scores, scores_to_levels_dict, generate_pattern
from backend.matcher import find_best_match

def test_full_evaluation_workflow():
    """测试完整评测流程（使用模拟答案）"""
    # 创建评测器
    evaluator = SBTEEvaluator(model_name="test-model")

    # 使用预定义答案（模拟模型回答）
    # 全部选择选项A（低分）
    answers = {f'q{i}': 1 for i in range(1, 31)}

    # 计算结果
    result = evaluator.compute_result(answers)

    # 验证结果结构
    assert 'model_name' in result
    assert 'raw_scores' in result
    assert 'levels' in result
    assert 'pattern' in result
    assert 'sbiti_type' in result
    assert 'chinese_name' in result

    # 验证分数范围
    for dim, score in result['raw_scores'].items():
        assert 2 <= score <= 6

    # 验证等级
    for dim, level in result['levels'].items():
        assert level in ['L', 'M', 'H']

    # 验证模式格式
    assert len(result['pattern'].replace('-', '')) == 15

def test_drunk_trigger():
    """测试酒鬼触发逻辑"""
    evaluator = SBTEEvaluator(model_name="test-model")

    # 触发酒鬼的答案
    answers = {f'q{i}': 2 for i in range(1, 31)}
    answers['drink_gate_q1'] = 3  # 饮酒
    answers['drink_gate_q2'] = 2  # 酒精令我信服

    result = evaluator.compute_result(answers)

    assert result['drunk_triggered'] == True
    assert result['sbiti_type'] == 'DRUNK'

def test_hhhh_trigger():
    """测试HHHH兜底逻辑"""
    evaluator = SBTEEvaluator(model_name="test-model")

    # 创建一个极低相似度的答案
    answers = {}
    for i in range(1, 31):
        if i % 2 == 0:
            answers[f'q{i}'] = 1  # L
        else:
            answers[f'q{i}'] = 3  # H

    result = evaluator.compute_result(answers)

    # 如果相似度很低，应该触发HHHH
    if result['match_similarity'] < 60:
        assert result['sbiti_type'] == 'HHHH'
        assert result['is_special'] == True

def test_save_and_load_results():
    """测试保存和加载结果"""
    evaluator = SBTEEvaluator(model_name="test-model")

    result = {
        'model_name': 'test-model',
        'sbiti_type': 'CTRL',
        'pattern': 'HHH-HMH-MHH-HHH-MHM'
    }

    test_file = 'data/test_integration_results.json'

    # 保存
    evaluator.save_result(result, output_file=test_file)

    # 加载并验证
    with open(test_file, 'r') as f:
        data = json.load(f)

    assert data['total_evaluations'] == 1
    assert len(data['evaluations']) == 1
    assert data['evaluations'][0]['model_name'] == 'test-model'

    # 清理
    Path(test_file).unlink()
```

- [ ] **Step 2: 运行集成测试**

```bash
pytest tests/test_integration.py -v
```

Expected: PASS

- [ ] **Step 3: 运行所有测试**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

- [ ] **Step 4: 提交代码**

```bash
git add tests/test_integration.py
git commit -m "test: add integration tests for end-to-end workflow"
```

---

## Task 10: 最终验证和文档完善

- [ ] **Step 1: 运行完整测试套件**

```bash
pytest tests/ -v --cov=backend
```

- [ ] **Step 2: 检查代码质量**

```bash
# 检查Python语法
python3 -m py_compile backend/*.py

# 检查bash脚本语法
bash -n batch_scripts/batch_eval.sh
```

- [ ] **Step 3: 验证.env配置**

```bash
# 确保.env文件存在且配置正确
test -f .env || echo "Warning: .env file not found"
```

- [ ] **Step 4: 创建使用示例**

```bash
# 创建示例文档
cat > USAGE.md << 'EOF'
# SBTI-Bench 使用指南

## 快速开始

### 1. 配置API密钥

编辑 `.env` 文件：
```
OPENROUTER_API_KEY=your_actual_api_key_here
DEFAULT_MODEL=openai/gpt-4
```

### 2. 评测单个模型

```bash
python -m backend.evaluator "GPT-4" "openai/gpt-4"
```

### 3. 批量评测

```bash
./batch_scripts/batch_eval.sh \
  "openai/gpt-4" \
  "anthropic/claude-3-sonnet" \
  "meta-llama/llama-3-70b"
```

## 查看结果

```bash
# 查看JSON结果
cat data/results.json | jq '.evaluations[-1]'

# 查看所有模型的SBTI类型
cat data/results.json | jq '.evaluations[] | {model: .model_name, type: .sbiti_type, name: .chinese_name}'
```

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
EOF
```

- [ ] **Step 5: 最终提交**

```bash
git add USAGE.md
git add .
git commit -m "feat: complete SBTI LLM benchmark system

- Implement question data extraction from HTML
- Add scoring logic with reverse scoring support
- Create type matching algorithm
- Integrate OpenRouter API with retry logic
- Build main evaluation script
- Add batch evaluation support
- Include comprehensive tests and documentation

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## 总结

本实施计划包含10个主要任务，覆盖了从项目初始化到最终测试的完整流程：

1. ✅ 项目初始化和依赖配置
2. ✅ 从HTML提取问题数据
3. ✅ 实现SBTI计分逻辑
4. ✅ 实现类型匹配算法
5. ✅ 实现OpenRouter API接口
6. ✅ 实现主评测脚本
7. ✅ 创建批量评测脚本
8. ✅ 创建项目文档
9. ✅ 运行集成测试
10. ✅ 最终验证和文档完善

**预计完成时间**: 2-3小时（取决于API调用速度）

**下一步**: 使用 `superpowers:subagent-driven-development` 或 `superpowers:executing-plans` 执行此计划。
