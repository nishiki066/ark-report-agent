# tests/test_log_filter.py
"""
测试日志过滤模块 - 查看原始日志
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.log_filter import view_raw_logs


def main():
    """主测试函数"""
    print("\n" + "🧪 " + "=" * 76)
    print("🧪 测试日志过滤模块 - 查看原始日志")
    print("🧪 " + "=" * 76)

    # 查看原始日志
    data = view_raw_logs()

    if not data:
        print("\n❌ 没有数据")
        return False

    # 分析日志特征
    print("\n" + "=" * 80)
    print("🔍 日志特征分析")
    print("=" * 80)

    print("\n💡 现在请仔细查看上面的原始日志,思考:")
    print("-" * 80)
    print("1. 哪些日志是重要的,必须保留?")
    print("2. 哪些日志是冗余的,可以过滤掉?")
    print("3. 是否需要对某些日志做特殊标记?")
    print("4. 是否需要提取某些关键信息?")
    print("-" * 80)

    # 给出一些观察建议
    if data['cn']:
        print("\n🇨🇳 中国区日志观察:")
        messages = [msg for _, msg in data['cn']['logs']]

        # 统计包含特定关键词的日志
        ssh_logs = [msg for msg in messages if 'ssh' in msg.lower() or '连接' in msg]
        error_logs = [msg for msg in messages if 'error' in msg.lower() or '错误' in msg or '失败' in msg]
        status_logs = [msg for msg in messages if '状态' in msg or 'status' in msg.lower()]

        print(f"   包含 SSH/连接 的日志: {len(ssh_logs)} 条")
        print(f"   包含 错误/失败 的日志: {len(error_logs)} 条")
        print(f"   包含 状态 的日志: {len(status_logs)} 条")

    if data['jp']:
        print("\n🇯🇵 日本区日志观察:")
        messages = [msg for _, msg in data['jp']['logs']]

        # 统计包含特定关键词的日志
        connect_logs = [msg for msg in messages if 'connected' in msg.lower() or 'authentication' in msg.lower()]
        maa_logs = [msg for msg in messages if 'maa' in msg.lower()]
        mumu_logs = [msg for msg in messages if 'mumu' in msg.lower()]
        completed_logs = [msg for msg in messages if '完成' in msg or 'completed' in msg.lower()]

        print(f"   包含 连接认证 的日志: {len(connect_logs)} 条")
        print(f"   包含 Maa 的日志: {len(maa_logs)} 条")
        print(f"   包含 Mumu 的日志: {len(mumu_logs)} 条")
        print(f"   包含 完成 的日志: {len(completed_logs)} 条")

    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("\n💡 下一步: 根据上面的日志内容,决定过滤规则")
    print("=" * 80 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)