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


def view_filtered_logs():
    """
    查看过滤后的日志内容
    """
    print("\n" + "=" * 80)
    print("📋 查看过滤后的日志内容")
    print("=" * 80)

    # 读取原始日志
    raw_data = get_latest_logs()

    if not raw_data['cn'] and not raw_data['jp']:
        print("\n⚠️  没有读取到任何数据")
        return None

    # 过滤日志
    filtered_data = filter_logs(raw_data)

    # 显示中国区
    if filtered_data['cn']:
        print("\n" + "=" * 80)
        print(f"🇨🇳 中国区 (arkcn_logs) - 过滤后")
        print("=" * 80)
        print(f"execution_id: {filtered_data['cn']['execution_id']}")
        print(f"开始时间: {filtered_data['cn']['start_time']}")
        print(f"结束时间: {filtered_data['cn']['end_time']}")
        print(f"日志总数: {len(filtered_data['cn']['logs'])} 条")
        print("\n" + "-" * 80)
        print("日志内容:")
        print("-" * 80)

        # ✅ 修改: 不显示编号,直接显示消息
        for message in filtered_data['cn']['logs']:
            print(message)

    # 显示日本区
    if filtered_data['jp']:
        print("\n" + "=" * 80)
        print(f"🇯🇵 日本区 (arkjp_logs) - 过滤后")
        print("=" * 80)
        print(f"execution_id: {filtered_data['jp']['execution_id']}")
        print(f"开始时间: {filtered_data['jp']['start_time']}")
        print(f"结束时间: {filtered_data['jp']['end_time']}")
        print(f"日志总数: {len(filtered_data['jp']['logs'])} 条")
        print("\n" + "-" * 80)
        print("日志内容:")
        print("-" * 80)

        # ✅ 修改: 不显示编号,直接显示消息
        for message in filtered_data['jp']['logs']:
            print(message)

    print("\n" + "=" * 80)
    print("✅ 过滤后的日志查看完成")
    print("=" * 80)

    return filtered_data


if __name__ == "__main__":
    """测试过滤功能"""
    print("\n🔍 启动日志过滤模块测试...")

    # 查看过滤后的日志
    filtered_data = view_filtered_logs()

    if filtered_data:
        # 统计信息
        cn_count = len(filtered_data['cn']['logs']) if filtered_data['cn'] else 0
        jp_count = len(filtered_data['jp']['logs']) if filtered_data['jp'] else 0

        print("\n" + "=" * 80)
        print("📊 统计信息")
        print("=" * 80)
        print(f"🇨🇳 中国区:")
        if filtered_data['cn']:
            start = filtered_data['cn']['start_time']
            end = filtered_data['cn']['end_time']
            duration = (end - start).total_seconds() if start and end else 0
            print(f"   开始: {start}")
            print(f"   结束: {end}")
            print(f"   耗时: {duration:.1f} 秒")
            print(f"   日志: {cn_count} 条")

        print(f"\n🇯🇵 日本区:")
        if filtered_data['jp']:
            start = filtered_data['jp']['start_time']
            end = filtered_data['jp']['end_time']
            duration = (end - start).total_seconds() if start and end else 0
            print(f"   开始: {start}")
            print(f"   结束: {end}")
            print(f"   耗时: {duration:.1f} 秒")
            print(f"   日志: {jp_count} 条")

        print(f"\n📈 总计: {cn_count + jp_count} 条日志")
        print("\n✅ 时间信息已提取,日志内容已清理")
        print("=" * 80 + "\n")