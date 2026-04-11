#!/usr/bin/env python3
"""
修复 results.json 中的中文名称显示错误
"""
import json
import sys
from pathlib import Path

def fix_results_json(file_path='data/results.json'):
    """修复 results.json 中的中文名称"""
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"处理文件: {file_path}")
    print(f"总评测数: {data['total_evaluations']}")

    fixed_count = 0
    for eval_data in data['evaluations']:
        sbiti_type = eval_data['sbiti_type']
        old_name = eval_data['chinese_name']

        # 如果中文名称和类型代码相同，说明有错误
        if old_name == sbiti_type:
            # 从 backend 导入正确的类型库
            from backend.questions import get_type_library
            type_library = get_type_library()

            # 获取正确的中文名称
            if sbiti_type in type_library:
                correct_name = type_library[sbiti_type]['cn']
                eval_data['chinese_name'] = correct_name
                print(f"  修复: {sbiti_type} '{old_name}' -> '{correct_name}'")
                fixed_count += 1

            # 处理特殊类型
            elif sbiti_type == 'HHHH':
                eval_data['chinese_name'] = '傻乐者'
                print(f"  修复: HHHH -> '傻乐者'")
                fixed_count += 1
            elif sbiti_type == 'DRUNK':
                eval_data['chinese_name'] = '酒鬼'
                print(f"  修复: DRUNK -> '酒鬼'")
                fixed_count += 1

    if fixed_count > 0:
        # 备份原文件
        backup_path = file_path.replace('.json', '_backup.json')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n已备份原文件到: {backup_path}")

        # 写入修复后的数据
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ 成功修复 {fixed_count} 条记录")
        print(f"✅ 已更新文件: {file_path}")
    else:
        print("✓ 没有需要修复的记录")

if __name__ == '__main__':
    fix_results_json()
