"""
测试scoring.py模块的计分逻辑
"""
import pytest
from backend.scoring import calculate_scores, scores_to_levels, generate_pattern, scores_to_levels_dict

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
    """测试生成模式字符串（简化测试）"""
    # 只测试基本功能
    levels = {
        'S1': 'L', 'S2': 'L', 'S3': 'L',
        'E1': 'L', 'E2': 'L', 'E3': 'L',
        'A1': 'L', 'A2': 'L', 'A3': 'L',
        'Ac1': 'L', 'Ac2': 'L', 'Ac3': 'L',
        'So1': 'L', 'So2': 'L', 'So3': 'L'
    }
    pattern = generate_pattern(levels)
    # 验证长度和分隔符
    assert len(pattern.replace('-', '')) == 15  # 15个字符
    assert pattern.count('-') == 4  # 4个分隔符
    assert pattern == 'LLL-LLL-LLL-LLL-LLL'  # 全L模式

def test_full_scoring_workflow():
    """测试完整计分流程（简化测试）"""
    # 简单测试：全选A选项
    answers = {f'q{i}': 1 for i in range(1, 31)}
    scores = calculate_scores(answers)
    levels = scores_to_levels_dict(scores)
    pattern = generate_pattern(levels)

    # 验证基本功能
    assert 'S1' in scores
    assert 'S1' in levels
    assert len(pattern) > 0
    assert pattern.count('-') == 4
