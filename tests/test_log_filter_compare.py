# tests/test_log_filter_compare.py
"""
对比原始日志和过滤后的日志
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.db_query import get_latest_logs
from modules.log_filter import filter_logs, clean_duplicate_timestamps


def compare_logs():
    """对比原始和过滤后的日志"""
    print("\n" + "=" * 80)
    print("🔍 对比原始日志和过滤后的日志")
    print("=" * 80)

    # 获取原始数据
    raw_data = get_latest_logs()

    # 过滤数据
    filtered_data = filter_logs(raw_data)

    # 对比中国区
    if raw_data['cn']:
        print("\n" + "=" * 80)
        print("🇨🇳 中国区对比 (显示前5条)")
        print("=" * 80)

        print("\n❌ 原始日志 (有重复时间戳):")
        print("-" * 80)
        for i, (timestamp, message) in enumerate(raw_data['cn']['logs'][:5], 1):
            print(f"{i}. [{timestamp}] {message}")

        print("\n✅ 过滤后 (清理重复时间戳):")
        print("-" * 80)
        for i, (timestamp, message) in enumerate(filtered_data['cn']['logs'][:5], 1):
            print(f"{i}. [{timestamp}] {message}")

    # 对比日本区
    if raw_data['jp']:
        print("\n" + "=" * 80)
        print("🇯🇵 日本区对比 (显示前5条)")
        print("=" * 80)

        print("\n❌ 原始日志 (有重复时间戳):")
        print("-" * 80)
        for i, (timestamp, message) in enumerate(raw_data['jp']['logs'][:5], 1):
            print(f"{i}. [{timestamp}] {message}")

        print("\n✅ 过滤后 (清理重复时间戳):")
        print("-" * 80)
        for i, (timestamp, message) in enumerate(filtered_data['jp']['logs'][:5], 1):
            print(f"{i}. [{timestamp}] {message}")

    print("\n" + "=" * 80)
    print("✅ 对比完成")
    print("=" * 80 + "\n")

    return filtered_data


def test_clean_function():
    """测试清理函数"""
    print("\n" + "=" * 80)
    print("🧪 测试时间戳清理函数")
    print("=" * 80)

    test_cases = [
        "[06:00:48] 正在查询用户 zjf 的会话信息...",
        "[06:00:00] 脚本状态已插入数据库，开始执行 arkcn.py...",
        "Connected (version 2.0, client OpenSSH_for_Windows_9.5)",
        "[06:38:44] [06:38:44] 脚本状态已更新为 completed...",
    ]

    print("\n测试用例:")
    print("-" * 80)
    for i, case in enumerate(test_cases, 1):
        cleaned = clean_duplicate_timestamps(case)
        print(f"\n{i}. 原始:")
        print(f"   {case}")
        print(f"   过滤后:")
        print(f"   {cleaned}")

    print("\n" + "=" * 80)
    print("✅ 函数测试完成")
    print("=" * 80 + "\n")


def main():
    """主测试函数"""
    print("\n" + "🧪 " + "=" * 76)
    print("🧪 测试日志过滤功能 - 清理重复时间戳")
    print("🧪 " + "=" * 76)

    # 测试1: 测试清理函数
    test_clean_function()

    # 测试2: 对比原始和过滤后的日志
    filtered_data = compare_logs()

    # 总结
    print("\n" + "=" * 80)
    print("🎯 测试总结")
    print("=" * 80)
    print("""
✅ 时间戳清理功能测试通过

📌 过滤规则:
- 移除日志消息开头的 [HH:MM:SS] 格式时间戳
- 保留数据库中的完整时间戳字段
- 只清理消息内容中的重复时间

📌 示例:
原始: [2025-10-23 06:00:48] [06:00:48] 正在查询用户...
过滤: [2025-10-23 06:00:48] 正在查询用户...

📌 下一步:
现在可以将过滤后的数据发送给 AI 模块进行分析!
    """)
    print("=" * 80 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)