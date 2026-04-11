"""
测试evaluator.py模块的主评测脚本
"""
import pytest
from unittest.mock import patch, MagicMock
from backend.evaluator import SBTEEvaluator
import json

@patch('backend.evaluator.LLMInterface')
def test_evaluator_init(mock_llm_class):
    """测试评测器初始化"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

    evaluator = SBTEEvaluator(model_name="test-model")
    assert evaluator.model_name == "test-model"

@patch('backend.evaluator.LLMInterface')
def test_evaluate_single_question(mock_llm_class):
    """测试评测单个问题"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_instance.evaluate_question.return_value = 2
    mock_llm_class.return_value = mock_instance

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

@patch('backend.evaluator.LLMInterface')
def test_compute_result(mock_llm_class):
    """测试计算评测结果"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

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

@patch('backend.evaluator.LLMInterface')
def test_save_result(mock_llm_class):
    """测试保存评测结果"""
    # Mock the LLMInterface class
    mock_instance = MagicMock()
    mock_llm_class.return_value = mock_instance

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
        assert data['evaluations'][0]['model_name'] == 'test-model'

    # 清理
    os.remove('data/test_results.json')
