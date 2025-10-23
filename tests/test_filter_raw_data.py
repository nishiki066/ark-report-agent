# tests/test_filter_raw_data.py
"""
查看 filter_logs() 返回的原始数据结构
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.db_query import get_latest_logs
from modules.log_filter import filter_logs
import json


def show_raw_data_structure():
    """显示原始数据结构"""
    print("\n" + "=" * 80)
    print("🔍 查看 filter_logs() 返回的原始数据结构")
    print("=" * 80)

    # 1. 读取数据
    print("\n📖 步骤1: 调用 get_latest_logs()")
    print("-" * 80)
    raw_data = get_latest_logs()
    print("返回类型:", type(raw_data))
    print("返回键:", list(raw_data.keys()))

    # 2. 过滤数据
    print("\n🔄 步骤2: 调用 filter_logs(raw_data)")
    print("-" * 80)
    filtered_data = filter_logs(raw_data)
    print("返回类型:", type(filtered_data))
    print("返回键:", list(filtered_data.keys()))

    # 3. 展示中国区数据结构
    if filtered_data['cn']:
        print("\n" + "=" * 80)
        print("🇨🇳 中国区数据结构详情")
        print("=" * 80)

        cn = filtered_data['cn']

        print("\n📦 数据类型:")
        print(f"   filtered_data['cn'] 的类型: {type(cn)}")

        print("\n📋 包含的键:")
        for key in cn.keys():
            print(f"   - {key}: {type(cn[key])}")

        print("\n📊 详细内容:")
        print(f"\n   execution_id:")
        print(f"      类型: {type(cn['execution_id'])}")
        print(f"      值: '{cn['execution_id']}'")

        print(f"\n   start_time:")
        print(f"      类型: {type(cn['start_time'])}")
        print(f"      值: {cn['start_time']}")

        print(f"\n   end_time:")
        print(f"      类型: {type(cn['end_time'])}")
        print(f"      值: {cn['end_time']}")

        print(f"\n   logs:")
        print(f"      类型: {type(cn['logs'])}")
        print(f"      长度: {len(cn['logs'])} 条")
        print(f"      每条日志的类型: {type(cn['logs'][0]) if cn['logs'] else 'N/A'}")

        print(f"\n   logs 内容示例 (前3条):")
        for i, log in enumerate(cn['logs'][:3], 1):
            print(f"      [{i}] 类型: {type(log)}")
            print(f"          长度: {len(log)} 字符")
            print(f"          内容: {log[:80]}...")
            print()

    # 4. 展示日本区数据结构
    if filtered_data['jp']:
        print("\n" + "=" * 80)
        print("🇯🇵 日本区数据结构详情")
        print("=" * 80)

        jp = filtered_data['jp']

        print("\n📦 数据类型:")
        print(f"   filtered_data['jp'] 的类型: {type(jp)}")

        print("\n📋 包含的键:")
        for key in jp.keys():
            print(f"   - {key}: {type(jp[key])}")

        print("\n📊 详细内容:")
        print(f"\n   execution_id:")
        print(f"      类型: {type(jp['execution_id'])}")
        print(f"      值: '{jp['execution_id']}'")

        print(f"\n   start_time:")
        print(f"      类型: {type(jp['start_time'])}")
        print(f"      值: {jp['start_time']}")

        print(f"\n   end_time:")
        print(f"      类型: {type(jp['end_time'])}")
        print(f"      值: {jp['end_time']}")

        print(f"\n   logs:")
        print(f"      类型: {type(jp['logs'])}")
        print(f"      长度: {len(jp['logs'])} 条")
        print(f"      每条日志的类型: {type(jp['logs'][0]) if jp['logs'] else 'N/A'}")

        print(f"\n   logs 内容示例 (前3条):")
        for i, log in enumerate(jp['logs'][:3], 1):
            print(f"      [{i}] 类型: {type(log)}")
            print(f"          长度: {len(log)} 字符")
            print(f"          内容: {log[:80]}...")
            print()

    # 5. 展示如何访问数据
    print("\n" + "=" * 80)
    print("💡 如何访问数据")
    print("=" * 80)

    print("\n示例代码:")
    print("-" * 80)
    print("""
# 获取过滤后的数据
filtered_data = filter_logs(raw_data)

# 访问中国区数据
if filtered_data['cn']:
    execution_id = filtered_data['cn']['execution_id']
    start_time = filtered_data['cn']['start_time']
    end_time = filtered_data['cn']['end_time']
    logs = filtered_data['cn']['logs']  # 这是一个列表

    # 遍历日志
    for message in logs:
        print(message)  # message 是字符串

    # 或者获取第一条日志
    first_log = logs[0]  # 字符串类型

    # 获取日志数量
    log_count = len(logs)
    """)

    print("\n实际运行:")
    print("-" * 80)
    if filtered_data['cn']:
        print(f"execution_id = '{filtered_data['cn']['execution_id']}'")
        print(f"start_time = {filtered_data['cn']['start_time']}")
        print(f"end_time = {filtered_data['cn']['end_time']}")
        print(f"log_count = {len(filtered_data['cn']['logs'])}")
        print(f"\n第一条日志:")
        print(f"  {filtered_data['cn']['logs'][0]}")
        print(f"\n最后一条日志:")
        print(f"  {filtered_data['cn']['logs'][-1]}")

    # 6. 展示 Python 字典结构
    print("\n" + "=" * 80)
    print("📦 完整的数据结构 (Python 字典格式)")
    print("=" * 80)

    # 创建一个简化版本用于展示
    simple_structure = {
        'cn': {
            'execution_id': filtered_data['cn']['execution_id'] if filtered_data['cn'] else None,
            'start_time': str(filtered_data['cn']['start_time']) if filtered_data['cn'] else None,
            'end_time': str(filtered_data['cn']['end_time']) if filtered_data['cn'] else None,
            'logs': [
                filtered_data['cn']['logs'][0][:60] + "..." if filtered_data['cn'] and filtered_data['cn'][
                    'logs'] else None,
                "...",
                filtered_data['cn']['logs'][-1][:60] + "..." if filtered_data['cn'] and filtered_data['cn'][
                    'logs'] else None
            ] if filtered_data['cn'] else None
        } if filtered_data['cn'] else None,
        'jp': {
            'execution_id': filtered_data['jp']['execution_id'] if filtered_data['jp'] else None,
            'start_time': str(filtered_data['jp']['start_time']) if filtered_data['jp'] else None,
            'end_time': str(filtered_data['jp']['end_time']) if filtered_data['jp'] else None,
            'logs': [
                filtered_data['jp']['logs'][0][:60] + "..." if filtered_data['jp'] and filtered_data['jp'][
                    'logs'] else None,
                "...",
                filtered_data['jp']['logs'][-1][:60] + "..." if filtered_data['jp'] and filtered_data['jp'][
                    'logs'] else None
            ] if filtered_data['jp'] else None
        } if filtered_data['jp'] else None
    }

    print("\n结构示意:")
    print(json.dumps(simple_structure, indent=2, ensure_ascii=False))

    print("\n" + "=" * 80)
    print("✅ 数据结构展示完成")
    print("=" * 80 + "\n")

    return filtered_data


if __name__ == "__main__":
    show_raw_data_structure()