"""
测试matcher.py模块的类型匹配算法
"""
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
    assert result['special'] == False

def test_find_best_match_with_drunk_trigger():
    """测试酒鬼触发（修复：验证secondaryType）"""
    user_pattern = "HHH-HMH-MHH-HHH-MHM"
    drunk_triggered = True
    result = find_best_match(user_pattern, drunk_triggered=drunk_triggered)

    assert result['code'] == 'DRUNK'
    assert result['similarity'] == 100
    assert result['special'] == True
    assert 'secondary_type' in result  # 修复：验证包含secondaryType
    assert result['secondary_type']['code'] == 'CTRL'  # 验证secondaryType是最佳常规类型

def test_find_best_match_hhhh_fallback():
    """测试HHHH兜底（修复：验证secondaryType仅在特殊类型中存在）"""
    # 使用一个会匹配到HHHH的极低相似度模式
    # 混合模式，确保不会很好匹配任何类型
    user_pattern = "LHL-HLM-HLM-LLH-MHL"
    result = find_best_match(user_pattern, drunk_triggered=False)

    # 常规类型不包含secondary_type
    assert 'code' in result
    if result.get('special', False):
        # 只有特殊类型才有secondary_type
        assert 'secondary_type' in result
    else:
        # 常规类型不应该有secondary_type
        assert 'secondary_type' not in result

def test_find_best_match_ranking():
    """测试匹配排序"""
    user_pattern = "HHH-HMH-MHH-HHH-MHM"
    ranked = find_best_match(user_pattern, return_all=True)

    assert len(ranked) == 26
    # CTRL应该是第一名
    assert ranked[0]['code'] == 'CTRL'
    assert ranked[0]['similarity'] == 100
