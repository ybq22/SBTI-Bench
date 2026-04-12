#!/usr/bin/env python3
"""
清理 results.json 中的重复评测记录
同一个 model_id 只保留最新的评测结果
"""
import json
from pathlib import Path
from datetime import datetime

def clean_results(input_file='data/results.json', output_file='data/results.json'):
    """
    清理评测结果，只保留每个model_id的最新记录

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    results_path = Path(input_file)

    if not results_path.exists():
        print(f"错误: 文件不存在 {input_file}")
        return

    # 读取数据
    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_count = len(data['evaluations'])
    print(f"原始评测记录数: {original_count}")

    # 统计每个model_id的记录数
    model_counts = {}
    for eval_data in data['evaluations']:
        model_id = eval_data['model_id']
        model_counts[model_id] = model_counts.get(model_id, 0) + 1

    # 显示重复的模型
    duplicates = {k: v for k, v in model_counts.items() if v > 1}
    if duplicates:
        print(f"\n发现重复的模型评测:")
        for model_id, count in sorted(duplicates.items(), key=lambda x: -x[1]):
            print(f"  {model_id}: {count} 条记录")
    else:
        print("\n✓ 没有重复记录")

    # 删除旧记录，只保留每个model_id的最新一条
    seen_models = {}
    unique_evaluations = []

    for eval_data in reversed(data['evaluations']):
        model_id = eval_data['model_id']

        if model_id not in seen_models:
            seen_models[model_id] = True
            unique_evaluations.append(eval_data)

    # 恢复时间顺序（最新在前）
    unique_evaluations.reverse()

    # 更新数据
    data['evaluations'] = unique_evaluations
    data['total_evaluations'] = len(unique_evaluations)
    data['last_updated'] = datetime.now().isoformat()

    # 备份原文件
    backup_path = results_path.with_suffix('.backup.json')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 保存清理后的数据
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n清理完成:")
    print(f"  原始记录: {original_count}")
    print(f"  清理后: {len(unique_evaluations)}")
    print(f"  删除记录: {original_count - len(unique_evaluations)}")
    print(f"  备份文件: {backup_path}")
    print(f"\n✓ 结果已保存到 {output_file}")

if __name__ == '__main__':
    clean_results()
