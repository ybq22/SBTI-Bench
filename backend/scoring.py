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
        模式字符串，如 "HHH-HMH-MHH-HHH-MHM"
    """
    levels_list = [levels[dim] for dim in DIMENSION_ORDER]
    groups = []

    # 每3个一组（15个维度 = 5组×3个）
    for i in range(0, len(levels_list), 3):
        groups.append(''.join(levels_list[i:i+3]))

    return '-'.join(groups)
