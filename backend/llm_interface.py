"""
OpenRouter API接口
"""
import os
import re
import time
import requests
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def parse_answer(response_text: str) -> int:
    """
    解析模型回答，提取选项值

    Args:
        response_text: 模型的原始回答

    Returns:
        选项值 (1-4)
    """
    text = response_text.strip()

    # 尝试提取大写字母A-D
    match = re.search(r'[A-D]', text.upper())
    if match:
        letter = match.group(0)
        return ord(letter) - ord('A') + 1

    # 尝试提取小写字母a-d
    match = re.search(r'[a-d]', text)
    if match:
        letter = match.group(0)
        return ord(letter) - ord('a') + 1

    # 无法解析，返回默认值2（M）
    return 2


class LLMInterface:
    """大语言模型接口"""

    # Paratera API支持的模型列表
    PARATERA_MODELS = ['Kimi-K2.5', 'moonshotai/kimi-k2.5']

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 120,
        base_url: Optional[str] = None
    ):
        """
        初始化LLM接口

        Args:
            api_key: API密钥（可选，默认根据模型自动选择）
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            timeout: 请求超时时间（秒）
            base_url: API基础URL（可选，默认根据模型自动选择）
        """
        self.model = model or os.getenv('DEFAULT_MODEL', 'openai/gpt-4')
        self.temperature = temperature or float(os.getenv('DEFAULT_TEMPERATURE', 0.7))
        self.max_tokens = max_tokens or int(os.getenv('DEFAULT_MAX_TOKENS', 1000))
        self.timeout = timeout or int(os.getenv('DEFAULT_TIMEOUT', 120))
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # 根据模型选择API配置
        self.use_paratera = self._should_use_paratera()

        if self.use_paratera:
            # 使用Paratera API
            self.api_key = api_key or os.getenv('PARATERA_API_KEY')
            self.base_url = base_url or os.getenv('PARATERA_BASE_URL', 'https://llmapi.paratera.com')
            if not self.api_key:
                raise ValueError("PARATERA_API_KEY is required for this model")
        else:
            # 使用OpenRouter API
            self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
            self.base_url = base_url or 'https://openrouter.ai/api/v1'
            if not self.api_key:
                raise ValueError("OPENROUTER_API_KEY is required")

    def _should_use_paratera(self) -> bool:
        """判断是否应该使用Paratera API"""
        return self.model in self.PARATERA_MODELS

    def call_model(self, prompt: str) -> str:
        """
        调用大语言模型

        Args:
            prompt: 提示词

        Returns:
            模型回答
        """
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )

                # 处理限流
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (2 ** attempt))
                        continue
                    else:
                        raise Exception("Rate limit exceeded")

                response.raise_for_status()
                result = response.json()

                # 提取回答
                content = result['choices'][0]['message']['content']
                return content.strip()

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise Exception("Request timeout")

            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise Exception(f"API call failed: {str(e)}")

        raise Exception("Max retries exceeded")

    def evaluate_question(self, question_text: str, options: list) -> int:
        """
        让模型回答一个问题

        Args:
            question_text: 问题文本
            options: 选项列表

        Returns:
            选择的选项值 (1-4)
        """
        # 构建提示词
        prompt = self._build_prompt(question_text, options)

        # 调用模型
        response = self.call_model(prompt)

        # 解析回答
        answer = parse_answer(response)

        return answer

    def _build_prompt(self, question_text: str, options: list) -> str:
        """构建提示词"""
        options_text = "\n".join([
            f"{chr(ord('A') + i)}. {opt['label']}"
            for i, opt in enumerate(options)
        ])

        prompt = f"""你正在参与一个关于自我认知、情感、态度、行动和社交倾向的心理测试。
请根据你的真实倾向选择最符合的答案。

{question_text}

{options_text}

对于这个问题，请只回答选项字母（A/B/C/D），不要添加其他解释。"""

        return prompt
