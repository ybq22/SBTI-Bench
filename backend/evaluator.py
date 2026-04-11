"""
SBTI评测主脚本
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from backend.questions import get_questions, get_special_questions, get_all_data
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
            # 优先使用 matcher 返回的中文名称，其次从类型库获取
            chinese_name = match_result.get('cn', sbiti_type)
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
