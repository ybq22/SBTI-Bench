"""
测试questions.py模块的数据提取功能
"""
import pytest
from backend.questions import (
    get_dimension_meta, get_questions, get_special_questions,
    get_normal_types, get_type_library, get_dim_explanations
)


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
    assert 'cn' in ctrl_type  # 包含中文名称


def test_type_library_exists():
    """验证TYPE_LIBRARY数据提取成功（修复：新增测试）"""
    library = get_type_library()
    assert 'CTRL' in library
    assert 'code' in library['CTRL']
    assert 'cn' in library['CTRL']
    assert 'desc' in library['CTRL']


def test_reverse_scoring_question():
    """验证q27是反向计分问题"""
    questions = get_questions()
    q27 = next(q for q in questions if q['id'] == 'q27')
    assert q27['dim'] == 'So2'
    assert '电子围栏' in q27['text']


def test_data_validation():
    """验证数据完整性检查"""
    # 正常情况不应抛出异常
    get_questions()
    get_normal_types()
    get_type_library()  # 修复：添加TYPE_LIBRARY测试
