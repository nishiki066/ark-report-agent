# modules/log_filter.py
"""
日志过滤模块 - 提取时间范围,清理日志中的时间戳
"""
import re
from modules.db_query import get_latest_logs


def clean_duplicate_timestamps(message):
    """
    清理日志消息中的时间戳

    Args:
        message: 原始日志消息

    Returns:
        清理后的消息(不含时间戳)
    """
    # 匹配形如 [HH:MM:SS] 的时间戳
    pattern = r'^\[\d{2}:\d{2}:\d{2}\]\s*'
    cleaned = re.sub(pattern, '', message)
    return cleaned


def filter_logs(data):
    """
    过滤日志
    - 提取开始和结束时间
    - 清理每条日志中的时间戳
    - 只保留消息内容

    Args:
        data: 从 get_latest_logs() 获取的原始数据

    Returns:
        过滤后的数据: {
            'cn': {
                'execution_id': str,
                'start_time': datetime,  # 开始时间
                'end_time': datetime,    # 结束时间
                'logs': [message1, message2, ...]  # 只有消息,没有时间戳
            },
            'jp': { ... }
        }
    """
    filtered_data = {
        'cn': None,
        'jp': None
    }

    # 处理中国区日志
    if data['cn']:
        logs = data['cn']['logs']

        # 提取开始和结束时间
        start_time = logs[0][0] if logs else None
        end_time = logs[-1][0] if logs else None

        # 清理时间戳,只保留消息
        cleaned_messages = [clean_duplicate_timestamps(message) for timestamp, message in logs]

        filtered_data['cn'] = {
            'execution_id': data['cn']['execution_id'],
            'start_time': start_time,
            'end_time': end_time,
            'logs': cleaned_messages
        }

    # 处理日本区日志
    if data['jp']:
        logs = data['jp']['logs']

        # 提取开始和结束时间
        start_time = logs[0][0] if logs else None
        end_time = logs[-1][0] if logs else None

        # 清理时间戳,只保留消息
        cleaned_messages = [clean_duplicate_timestamps(message) for timestamp, message in logs]

        filtered_data['jp'] = {
            'execution_id': data['jp']['execution_id'],
            'start_time': start_time,
            'end_time': end_time,
            'logs': cleaned_messages
        }

    return filtered_data

