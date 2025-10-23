# tests/test_db_query.py
"""
测试数据库查询模块
验证所有查询功能是否正常工作
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.db_query import DatabaseQuery, get_latest_data_for_ai, get_latest_logs_summary


def print_separator(title):
    """打印分隔线"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def test_database_connection():
    """测试1: 数据库连接"""
    print_separator("测试 1: 数据库连接")

    try:
        with DatabaseQuery() as db:
            if db.connection:
                print("✅ 数据库连接成功!")
                return True
            else:
                print("❌ 数据库连接失败!")
                return False
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return False


def test_get_latest_execution_ids():
    """测试2: 获取最新的 execution_id"""
    print_separator("测试 2: 获取最新的 execution_id")

    try:
        with DatabaseQuery() as db:
            # 测试中国区
            print("\n🔍 查询 arkcn_logs 最新 execution_id...")
            cn_result = db.get_latest_execution_id('arkcn_logs')

            if cn_result:
                execution_id, timestamp = cn_result
                print(f"✅ 中国区:")
                print(f"   execution_id: {execution_id}")
                print(f"   最新时间: {timestamp}")
            else:
                print("⚠️  中国区未找到数据")

            # 测试日本区
            print("\n🔍 查询 arkjp_logs 最新 execution_id...")
            jp_result = db.get_latest_execution_id('arkjp_logs')

            if jp_result:
                execution_id, timestamp = jp_result
                print(f"✅ 日本区:")
                print(f"   execution_id: {execution_id}")
                print(f"   最新时间: {timestamp}")
            else:
                print("⚠️  日本区未找到数据")

            return bool(cn_result or jp_result)

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False


def test_get_logs_by_execution_id():
    """测试3: 根据 execution_id 获取日志"""
    print_separator("测试 3: 根据 execution_id 获取日志详情")

    try:
        with DatabaseQuery() as db:
            # 获取中国区最新 execution_id
            cn_result = db.get_latest_execution_id('arkcn_logs')

            if cn_result:
                execution_id, _ = cn_result
                print(f"\n🔍 获取中国区 execution_id={execution_id} 的所有日志...")

                logs = db.get_logs_by_execution_id('arkcn_logs', execution_id)
                print(f"✅ 共获取 {len(logs)} 条日志")

                if logs:
                    print(f"\n📋 显示前3条日志:")
                    for i, log in enumerate(logs[:3], 1):
                        log_id, exec_id, timestamp, message = log
                        short_msg = (message[:50] + '...') if len(message) > 50 else message
                        print(f"   {i}. [{timestamp}] {short_msg}")

                    if len(logs) > 3:
                        print(f"   ... (还有 {len(logs) - 3} 条)")

                return True
            else:
                print("⚠️  未找到中国区数据")
                return False

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False


def test_get_latest_cn_logs():
    """测试4: 获取中国区最新日志"""
    print_separator("测试 4: 获取中国区最新完整日志数据")

    try:
        with DatabaseQuery() as db:
            print("\n🔍 获取中国区最新日志...")
            data = db.get_latest_cn_logs()

            print(f"\n📊 中国区数据:")
            print(f"   execution_id: {data['execution_id']}")
            print(f"   时间戳: {data['timestamp']}")
            print(f"   日志条数: {data['log_count']}")

            if data['logs']:
                print(f"\n📋 日志样例 (前3条):")
                for i, log in enumerate(data['logs'][:3], 1):
                    _, _, timestamp, message = log
                    short_msg = (message[:50] + '...') if len(message) > 50 else message
                    print(f"   {i}. [{timestamp}] {short_msg}")

            return data['log_count'] > 0

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False


def test_get_latest_jp_logs():
    """测试5: 获取日本区最新日志"""
    print_separator("测试 5: 获取日本区最新完整日志数据")

    try:
        with DatabaseQuery() as db:
            print("\n🔍 获取日本区最新日志...")
            data = db.get_latest_jp_logs()

            print(f"\n📊 日本区数据:")
            print(f"   execution_id: {data['execution_id']}")
            print(f"   时间戳: {data['timestamp']}")
            print(f"   日志条数: {data['log_count']}")

            if data['logs']:
                print(f"\n📋 日志样例 (前3条):")
                for i, log in enumerate(data['logs'][:3], 1):
                    _, _, timestamp, message = log
                    short_msg = (message[:50] + '...') if len(message) > 50 else message
                    print(f"   {i}. [{timestamp}] {short_msg}")

            return data['log_count'] > 0

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False


def test_get_latest_both_logs():
    """测试6: 同时获取两个区的最新日志"""
    print_separator("测试 6: 同时获取中国区和日本区最新日志")

    try:
        with DatabaseQuery() as db:
            print("\n🔍 同时获取两个区的最新日志...")
            data = db.get_latest_both_logs()

            print(f"\n🇨🇳 中国区:")
            print(f"   execution_id: {data['cn']['execution_id']}")
            print(f"   时间: {data['cn']['timestamp']}")
            print(f"   日志数: {data['cn']['log_count']}")

            print(f"\n🇯🇵 日本区:")
            print(f"   execution_id: {data['jp']['execution_id']}")
            print(f"   时间: {data['jp']['timestamp']}")
            print(f"   日志数: {data['jp']['log_count']}")

            print(f"\n📊 总计: {data['total_logs']} 条日志")

            return data['total_logs'] > 0

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False


def test_format_logs_for_ai():
    """测试7: 格式化日志用于 AI"""
    print_separator("测试 7: 格式化日志为 AI 可读格式")

    try:
        with DatabaseQuery() as db:
            print("\n🔍 获取并格式化中国区日志...")
            cn_data = db.get_latest_cn_logs()

            if cn_data['logs']:
                formatted = db.format_logs_for_ai(cn_data['logs'])

                print(f"\n✅ 格式化完成!")
                print(f"原始数据: {len(cn_data['logs'])} 条日志")
                print(f"格式化文本: {len(formatted)} 字符")

                print(f"\n📝 格式化文本预览 (前5行):")
                lines = formatted.split('\n')[:5]
                for line in lines:
                    print(f"   {line}")

                if len(formatted.split('\n')) > 5:
                    print(f"   ... (还有 {len(formatted.split('\n')) - 5} 行)")

                return True
            else:
                print("⚠️  没有日志可格式化")
                return False

    except Exception as e:
        print(f"❌ 格式化失败: {e}")
        return False


def test_get_formatted_data_for_ai():
    """测试8: 获取用于 AI 处理的完整数据"""
    print_separator("测试 8: 获取完整的 AI 处理数据包")

    try:
        print("\n🔍 获取完整的 AI 数据包...")
        data = get_latest_data_for_ai()

        print(f"\n📦 数据包内容:")
        print(f"\n🇨🇳 中国区:")
        print(f"   execution_id: {data['cn']['execution_id']}")
        print(f"   时间: {data['cn']['timestamp']}")
        print(f"   日志数: {data['cn']['log_count']}")
        print(f"   格式化文本: {len(data['cn']['formatted_logs'])} 字符")

        print(f"\n🇯🇵 日本区:")
        print(f"   execution_id: {data['jp']['execution_id']}")
        print(f"   时间: {data['jp']['timestamp']}")
        print(f"   日志数: {data['jp']['log_count']}")
        print(f"   格式化文本: {len(data['jp']['formatted_logs'])} 字符")

        print(f"\n📝 中国区日志预览 (前3行):")
        cn_lines = data['cn']['formatted_logs'].split('\n')[:3]
        for line in cn_lines:
            print(f"   {line}")

        print(f"\n📝 日本区日志预览 (前3行):")
        jp_lines = data['jp']['formatted_logs'].split('\n')[:3]
        for line in jp_lines:
            print(f"   {line}")

        print(f"\n✅ 这些数据可以直接发送给 AI 进行分析!")

        return True

    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return False


def test_get_execution_summary():
    """测试9: 获取执行摘要"""
    print_separator("测试 9: 获取执行摘要和统计信息")

    try:
        print("\n🔍 获取最新日志的摘要信息...")
        summary = get_latest_logs_summary()

        if summary['cn']:
            print(f"\n🇨🇳 中国区摘要:")
            print(f"   开始时间: {summary['cn']['start_time']}")
            print(f"   结束时间: {summary['cn']['end_time']}")
            print(f"   总日志数: {summary['cn']['total_logs']}")
            print(f"   错误数量: {summary['cn']['error_count']}")
            print(f"   成功标识: {len(summary['cn']['success_indicators'])} 个")

            if summary['cn']['success_indicators']:
                print(f"\n   ✅ 成功标识样例:")
                for indicator in summary['cn']['success_indicators'][:3]:
                    short = (indicator[:50] + '...') if len(indicator) > 50 else indicator
                    print(f"      - {short}")

        if summary['jp']:
            print(f"\n🇯🇵 日本区摘要:")
            print(f"   开始时间: {summary['jp']['start_time']}")
            print(f"   结束时间: {summary['jp']['end_time']}")
            print(f"   总日志数: {summary['jp']['total_logs']}")
            print(f"   错误数量: {summary['jp']['error_count']}")
            print(f"   成功标识: {len(summary['jp']['success_indicators'])} 个")

            if summary['jp']['success_indicators']:
                print(f"\n   ✅ 成功标识样例:")
                for indicator in summary['jp']['success_indicators'][:3]:
                    short = (indicator[:50] + '...') if len(indicator) > 50 else indicator
                    print(f"      - {short}")

        return bool(summary['cn'] or summary['jp'])

    except Exception as e:
        print(f"❌ 获取摘要失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀 " + "=" * 66)
    print("🚀 开始测试数据库查询模块")
    print("🚀 " + "=" * 66)

    tests = [
        ("数据库连接", test_database_connection),
        ("获取最新 execution_id", test_get_latest_execution_ids),
        ("根据 execution_id 获取日志", test_get_logs_by_execution_id),
        ("获取中国区最新日志", test_get_latest_cn_logs),
        ("获取日本区最新日志", test_get_latest_jp_logs),
        ("同时获取两区日志", test_get_latest_both_logs),
        ("格式化日志", test_format_logs_for_ai),
        ("获取 AI 数据包", test_get_formatted_data_for_ai),
        ("获取执行摘要", test_get_execution_summary),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ 测试异常: {e}")
            results.append((name, False))

    # 打印测试总结
    print_separator("测试总结")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n测试结果: {passed}/{total} 通过\n")

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status}  {name}")

    # 最终结论
    print("\n" + "=" * 70)
    if passed == total:
        print("🎉 所有测试通过! 查询模块工作正常!")
        print("✨ 可以开始开发 AI 处理模块了!")
    else:
        print(f"⚠️  {total - passed} 个测试失败,请检查问题")
    print("=" * 70 + "\n")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)