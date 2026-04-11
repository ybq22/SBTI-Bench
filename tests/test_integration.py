"""
集成测试 - 测试完整的评测流程
"""
import pytest
import json
from pathlib import Path
from backend.evaluator import SBTEEvaluator
from backend.questions import get_questions
from backend.scoring import calculate_scores, scores_to_levels_dict, generate_pattern
from backend.matcher import find_best_match
from unittest.mock import patch, MagicMock

@patch('backend.evaluator.LLMInterface')
def test_full_evaluation_workflow(mock_llm_class):
    """测试完整评测流程（使用模拟答案）"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

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

@patch('backend.evaluator.LLMInterface')
def test_drunk_trigger(mock_llm_class):
    """测试酒鬼触发逻辑"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

    evaluator = SBTEEvaluator(model_name="test-model")

    # 触发酒鬼的答案
    answers = {f'q{i}': 2 for i in range(1, 31)}
    answers['drink_gate_q1'] = 3  # 饮酒
    answers['drink_gate_q2'] = 2  # 酒精令我信服

    result = evaluator.compute_result(answers)

    assert result['drunk_triggered'] == True
    assert result['sbiti_type'] == 'DRUNK'

@patch('backend.evaluator.LLMInterface')
def test_hhhh_trigger(mock_llm_class):
    """测试HHHH兜底逻辑"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

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

@patch('backend.evaluator.LLMInterface')
def test_save_and_load_results(mock_llm_class):
    """测试保存和加载结果"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

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

def test_questions_to_scoring_to_matching_integration():
    """测试问题→计分→匹配的完整流程"""
    # 获取问题
    questions = get_questions()
    assert len(questions) == 30

    # 模拟答案（全部选2，中立）
    answers = {q['id']: 2 for q in questions}

    # 计算分数
    scores = calculate_scores(answers)

    # 转换为等级
    levels = scores_to_levels_dict(scores)

    # 生成模式
    pattern = generate_pattern(levels)

    # 匹配类型
    match = find_best_match(pattern)

    # 验证流程
    assert len(scores) == 15
    assert len(levels) == 15
    assert len(pattern.replace('-', '')) == 15
    assert 'code' in match
    assert 'similarity' in match
