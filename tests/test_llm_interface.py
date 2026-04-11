"""
测试llm_interface.py模块的OpenRouter API接口
"""
import pytest
from unittest.mock import patch, MagicMock
from backend.llm_interface import LLMInterface, parse_answer

def test_parse_answer_simple():
    """测试解析简单字母答案"""
    assert parse_answer("A") == 1
    assert parse_answer("B") == 2
    assert parse_answer("C") == 3
    # Note: SBTI only has 3 options (A/B/C), but we handle D for robustness
    assert parse_answer("D") == 4

def test_parse_answer_with_text():
    """测试解析包含文字的答案"""
    assert parse_answer("我选择A") == 1
    assert parse_answer("答案是B") == 2
    assert parse_answer("选C") == 3

def test_parse_answer_lowercase():
    """测试解析小写字母"""
    assert parse_answer("a") == 1
    assert parse_answer("b") == 2
    assert parse_answer("c") == 3

def test_parse_answer_invalid():
    """测试解析无效答案"""
    assert parse_answer("我不知道") == 2  # 默认返回M
    assert parse_answer("") == 2
    assert parse_answer("E") == 2  # 超出范围

def test_llm_interface_init():
    """测试LLM接口初始化"""
    interface = LLMInterface(api_key="test_key")
    assert interface.api_key == "test_key"
    assert interface.model == "openai/gpt-4"

@patch('backend.llm_interface.requests.post')
def test_call_model_success(mock_post):
    """测试成功调用模型"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [{
            'message': {
                'content': 'A'
            }
        }]
    }
    mock_post.return_value = mock_response

    interface = LLMInterface(api_key="test_key")
    result = interface.call_model("test prompt")

    assert result == 'A'

@patch('backend.llm_interface.requests.post')
def test_call_model_with_retry(mock_post):
    """测试API调用重试机制"""
    # 第一次失败，第二次成功
    mock_post.side_effect = [
        MagicMock(status_code=429),  # 限流
        MagicMock(status_code=200, json=lambda: {'choices': [{'message': {'content': 'B'}}]})
    ]

    interface = LLMInterface(api_key="test_key", max_retries=2)
    result = interface.call_model("test prompt")

    assert result == 'B'
    assert mock_post.call_count == 2
