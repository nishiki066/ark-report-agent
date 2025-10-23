# tests/test_filtered_format.py
"""
测试新的过滤格式 - 只保留开始/结束时间,移除日志中的时间戳
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.db_query import get_latest_logs
from modules.log_filter import filter_logs


def test_filter_format():
    """测试过滤后的数据格式"""
    print("\n" + "=" * 80)
    print("🧪 测试新的过滤格式")
    print("=" * 80)

    # 获取原始数据
    print("\n📖 读取原始数据...")
    raw_data = get_latest_logs()

    # 过滤数据
    print("🔄 过滤数据...")
    filtered_data = filter_logs(raw_data)

    # 对比中国区
    if raw_data['cn']:
        print("\n" + "=" * 80)
        print("🇨🇳 中国区对比")
        print("=" * 80)

        print("\n❌ 原始格式 (前3条):")
        print("-" * 80)
        for i, (timestamp, message) in enumerate(raw_data['cn']['logs'][:3], 1):
            print(f"{i}. [{timestamp}] {message}")

        print("\n✅ 过滤后格式:")
        print("-" * 80)
        print(f"execution_id: {filtered_data['cn']['execution_id']}")
        print(f"开始时间: {filtered_data['cn']['start_time']}")
        print(f"结束时间: {filtered_data['cn']['end_time']}")
        print(f"\n日志内容 (前3条):")
        for i, message in enumerate(filtered_data['cn']['logs'][:3], 1):
            print(f"{i}. {message}")

    # 对比日本区
    if raw_data['jp']:
        print("\n" + "=" * 80)
        print("🇯🇵 日本区对比")
        print("=" * 80)

        print("\n❌ 原始格式 (前3条):")
        print("-" * 80)
        for i, (timestamp, message) in enumerate(raw_data['jp']['logs'][:3], 1):
            print(f"{i}. [{timestamp}] {message}")

        print("\n✅ 过滤后格式:")
        print("-" * 80)
        print(f"execution_id: {filtered_data['jp']['execution_id']}")
        print(f"开始时间: {filtered_data['jp']['start_time']}")
        print(f"结束时间: {filtered_data['jp']['end_time']}")
        print(f"\n日志内容 (前3条):")
        for i, message in enumerate(filtered_data['jp']['logs'][:3], 1):
            print(f"{i}. {message}")

    # 验证数据结构
    print("\n" + "=" * 80)
    print("📊 数据结构验证")
    print("=" * 80)

    if filtered_data['cn']:
        print("\n✅ 中国区数据结构:")
        print(f"   - execution_id: {type(filtered_data['cn']['execution_id'])}")
        print(f"   - start_time: {type(filtered_data['cn']['start_time'])}")
        print(f"   - end_time: {type(filtered_data['cn']['end_time'])}")
        print(f"   - logs: {type(filtered_data['cn']['logs'])} (长度: {len(filtered_data['cn']['logs'])})")
        print(f"   - logs[0]: {type(filtered_data['cn']['logs'][0])}")

    if filtered_data['jp']:
        print("\n✅ 日本区数据结构:")
        print(f"   - execution_id: {type(filtered_data['jp']['execution_id'])}")
        print(f"   - start_time: {type(filtered_data['jp']['start_time'])}")
        print(f"   - end_time: {type(filtered_data['jp']['end_time'])}")
        print(f"   - logs: {type(filtered_data['jp']['logs'])} (长度: {len(filtered_data['jp']['logs'])})")
        print(f"   - logs[0]: {type(filtered_data['jp']['logs'][0])}")

    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("\n💡 新格式说明:")
    print("   - 开始/结束时间单独保存")
    print("   - 日志内容不包含时间戳")
    print("   - 数据更简洁,适合 AI 分析")
    print("=" * 80 + "\n")

    return filtered_data


if __name__ == "__main__":
    test_filter_format()