"""
SBTI类型匹配算法
"""
from typing import List, Dict, Any
from backend.questions import get_normal_types, get_type_library

# 类型库缓存
_NORMAL_TYPES = None
_TYPE_LIBRARY = None


def _get_normal_types() -> List[Dict[str, str]]:
    """获取常规类型（带缓存）"""
    global _NORMAL_TYPES
    if _NORMAL_TYPES is None:
        _NORMAL_TYPES = get_normal_types()
    return _NORMAL_TYPES


def _get_type_library() -> Dict[str, Dict[str, str]]:
    """获取类型库（带缓存）"""
    global _TYPE_LIBRARY
    if _TYPE_LIBRARY is None:
        _TYPE_LIBRARY = get_type_library()
    return _TYPE_LIBRARY


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
    查找最佳匹配的SBTI类型（修复：正确实现secondaryType）

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
            'cn': type_info.get('cn', type_info['code']),
            'distance': distance,
            'exact': exact,
            'similarity': similarity
        })

    # 排序：距离升序，精确匹配降序，相似度降序
    ranked.sort(key=lambda x: (x['distance'], -x['exact'], -x['similarity']))

    if return_all:
        return ranked

    # 获取最佳常规匹配
    best_normal = ranked[0]

    # 处理特殊类型（修复：正确实现secondaryType）
    if drunk_triggered:
        # DRUNK类型触发
        return {
            'code': 'DRUNK',
            'cn': '酒鬼',
            'pattern': user_pattern,
            'similarity': 100,
            'exact': 15,
            'special': True,
            'secondary_type': best_normal  # 修复：保存最佳常规类型作为secondaryType
        }

    # HHHH触发检查
    if best_normal['similarity'] < 60:
        # HHHH兜底类型
        return {
            'code': 'HHHH',
            'cn': '傻乐者',
            'pattern': user_pattern,
            'similarity': best_normal['similarity'],
            'exact': best_normal['exact'],
            'special': True,
            'secondary_type': best_normal  # 修复：保存最佳常规类型作为secondaryType
        }

    # 常规类型
    return {
        'code': best_normal['code'],
        'cn': best_normal['cn'],
        'pattern': best_normal['pattern'],
        'similarity': best_normal['similarity'],
        'exact': best_normal['exact'],
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
