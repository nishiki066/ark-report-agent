# modules/ai_processor.py
"""
AI 处理模块 - 使用 DeepSeek API 分析日志并生成报告
"""
import requests
import json
import time
import sys
import os
from config.database import AI_CONFIG
from datetime import datetime

# ============================================================================
# 提示词配置区域 - 可以在这里自定义提示词
# ============================================================================
def load_prompt_from_file(filename):
    """
    从文件加载提示词

    Args:
        filename: 文件名（相对于 prompts/ 目录）

    Returns:
        文件内容字符串
    """
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    prompt_file = os.path.join(project_root, 'prompts', filename)

    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"提示词文件未找到: {prompt_file}")
    except Exception as e:
        raise Exception(f"读取提示词文件失败: {e}")


# 从文件加载提示词
try:
    SYSTEM_PROMPT = load_prompt_from_file('system_prompt.txt')
    USER_PROMPT_TEMPLATE = load_prompt_from_file('user_prompt.txt')
except Exception as e:
    print(f"⚠️  警告: {e}")



# ============================================================================
# 以下是功能代码 - 一般不需要修改
# ============================================================================

def check_balance(show_detail=True):
    """
    查询 DeepSeek API 账户余额

    Args:
        show_detail: 是否显示详细信息

    Returns:
        dict: 余额信息
    """
    api_key = AI_CONFIG['deepseek_api_key']

    if not api_key:
        raise ValueError("未配置 DEEPSEEK_API_KEY，请在 .env 文件中添加")

    url = f"{AI_CONFIG['api_base']}/user/balance"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        balance_data = response.json()

        if show_detail:
            print("\n" + "=" * 80)
            print("💰 DeepSeek API 余额信息")
            print("=" * 80)

            if balance_data.get('is_available'):
                print("✅ 账户状态: 可用")
            else:
                print("⚠️  账户状态: 不可用")

            balance_infos = balance_data.get('balance_infos', [])

            if balance_infos:
                for info in balance_infos:
                    currency = info.get('currency', 'CNY')
                    total = info.get('total_balance', '0.00')
                    granted = info.get('granted_balance', '0.00')
                    topped_up = info.get('topped_up_balance', '0.00')

                    print(f"\n币种: {currency}")
                    print(f"   总余额: {total}")
                    print(f"   赠送余额: {granted}")
                    print(f"   充值余额: {topped_up}")
            else:
                print("\n未找到余额信息")

            print("=" * 80 + "\n")

        return balance_data

    except requests.exceptions.RequestException as e:
        raise Exception(f"查询余额失败: {e}")


def format_logs_for_ai(filtered_data):
    """
    将过滤后的数据格式化为发送给 AI 的文本

    Args:
        filtered_data: 从 filter_logs() 获取的数据

    Returns:
        格式化的文本字符串
    """
    lines = []

    # 中国区
    if filtered_data['cn']:
        cn = filtered_data['cn']
        lines.append("【中国区 (arkcn)】")
        lines.append(f"执行ID: {cn['execution_id']}")
        lines.append(f"开始时间: {cn['start_time']}")
        lines.append(f"结束时间: {cn['end_time']}")
        lines.append(f"日志条数: {len(cn['logs'])} 条")
        lines.append("")
        lines.append("执行日志:")
        lines.extend(cn['logs'])
        lines.append("")

    # 日本区
    if filtered_data['jp']:
        jp = filtered_data['jp']
        lines.append("【日本区 (arkjp)】")
        lines.append(f"执行ID: {jp['execution_id']}")
        lines.append(f"开始时间: {jp['start_time']}")
        lines.append(f"结束时间: {jp['end_time']}")
        lines.append(f"日志条数: {len(jp['logs'])} 条")
        lines.append("")
        lines.append("执行日志:")
        lines.extend(jp['logs'])
        lines.append("")

    return "\n".join(lines)


def create_prompt(log_content):
    """
    创建发送给 AI 的 Prompt
    使用顶部定义的提示词模板

    Args:
        log_content: 格式化后的日志内容

    Returns:
        完整的 prompt
    """
    # 使用模板填充日志内容
    prompt = USER_PROMPT_TEMPLATE.format(log_content=log_content)
    return prompt


def show_current_prompts():
    """显示当前使用的提示词"""
    print("\n" + "=" * 80)
    print("📝 当前系统提示词:")
    print("=" * 80)
    print(SYSTEM_PROMPT)

    print("\n" + "=" * 80)
    print("📝 当前用户提示词模板:")
    print("=" * 80)
    print(USER_PROMPT_TEMPLATE)
    print("=" * 80 + "\n")


def reload_prompts():
    """重新加载提示词文件"""
    global SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

    try:
        SYSTEM_PROMPT = load_prompt_from_file('system_prompt.txt')
        USER_PROMPT_TEMPLATE = load_prompt_from_file('user_prompt.txt')
        print("✅ 提示词已重新加载")
        return True
    except Exception as e:
        print(f"❌ 重新加载失败: {e}")
        return False


def show_progress(start_time):
    """
    显示简单的进度信息(时间计时)

    Args:
        start_time: 开始时间

    Returns:
        经过的时间(秒)
    """
    elapsed = time.time() - start_time
    return elapsed


def call_deepseek_api_stream(prompt, show_time=True):
    """
    调用 DeepSeek API (流式输出)
    实时显示 AI 生成的内容,并显示计时

    Args:
        prompt: 要发送的 prompt
        show_time: 是否显示计时信息

    Returns:
        AI 生成的完整回复文本
    """
    api_key = AI_CONFIG['deepseek_api_key']

    if not api_key:
        raise ValueError("未配置 DEEPSEEK_API_KEY，请在 .env 文件中添加")

    url = f"{AI_CONFIG['api_base']}/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # 构建消息 - 启用流式输出
    data = {
        'model': 'deepseek-chat',  # 使用快速模式
        'messages': [
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.7,  # 适中的温度,快速响应
        'max_tokens': 2000,
        'stream': True  # 启用流式输出
    }

    try:
        start_time = time.time()

        # 发送请求,启用流式传输
        response = requests.post(url, headers=headers, json=data, stream=True, timeout=120)
        response.raise_for_status()

        full_content = []
        char_count = 0

        print("\n" + "=" * 80)
        if show_time:
            print("🤖 AI 实时输出 [计时开始...]")
        else:
            print("🤖 AI 实时输出:")
        print("=" * 80)

        # 逐行读取流式响应
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')

                # 跳过注释行
                if line.startswith(':'):
                    continue

                # 移除 "data: " 前缀
                if line.startswith('data: '):
                    line = line[6:]

                # 检查是否是结束标记
                if line == '[DONE]':
                    break

                try:
                    # 解析 JSON
                    chunk = json.loads(line)

                    # 提取内容
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        delta = chunk['choices'][0].get('delta', {})
                        content = delta.get('content', '')

                        if content:
                            # 实时打印内容
                            print(content, end='', flush=True)
                            full_content.append(content)
                            char_count += len(content)

                except json.JSONDecodeError:
                    # 忽略无法解析的行
                    continue

        # 计算总耗时
        total_time = time.time() - start_time

        print("\n" + "=" * 80)
        if show_time:
            print(f"⏱️  生成完成! 耗时: {total_time:.2f} 秒 | 字符数: {char_count}")
        print("=" * 80)

        # 返回完整内容
        return ''.join(full_content)

    except requests.exceptions.RequestException as e:
        raise Exception(f"调用 DeepSeek API 失败: {e}")


def call_deepseek_api(prompt):
    """
    调用 DeepSeek API (普通模式,一次性返回)

    Args:
        prompt: 要发送的 prompt

    Returns:
        AI 生成的回复文本
    """
    api_key = AI_CONFIG['deepseek_api_key']

    if not api_key:
        raise ValueError("未配置 DEEPSEEK_API_KEY，请在 .env 文件中添加")

    url = f"{AI_CONFIG['api_base']}/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'deepseek-chat',  # 使用快速模式
        'messages': [
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.7,
        'max_tokens': 2000
    }

    try:
        start_time = time.time()
        print("\n⏳ 等待 AI 响应...")

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        total_time = time.time() - start_time

        result = response.json()
        content = result['choices'][0]['message']['content']

        print(f"✅ 响应完成! 耗时: {total_time:.2f} 秒")

        return content

    except requests.exceptions.RequestException as e:
        raise Exception(f"调用 DeepSeek API 失败: {e}")


def process_with_ai(filtered_data, stream=True, show_time=True):
    """
    使用 AI 处理日志数据，生成报告

    Args:
        filtered_data: 从 filter_logs() 获取的过滤后数据
        stream: 是否使用流式输出 (默认 True)
        show_time: 是否显示计时信息 (默认 True)

    Returns:
        AI 生成的报告文本
    """
    print("\n📝 格式化日志数据...")
    log_content = format_logs_for_ai(filtered_data)

    print("🤖 创建 AI Prompt...")
    prompt = create_prompt(log_content)

    if stream:
        print("🚀 调用 DeepSeek API (流式输出)...")
        report = call_deepseek_api_stream(prompt, show_time=show_time)
    else:
        print("🚀 调用 DeepSeek API (普通模式)...")
        report = call_deepseek_api(prompt)
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80)

    print("\n✅ AI 报告生成完成!")

    return report
