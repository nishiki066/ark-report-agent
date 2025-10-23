# tests/test_db_query_module.py
"""
测试 db_query 模块的功能
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.db_query import get_latest_logs


def test_get_latest_logs():
    """测试获取最新日志功能"""
    print("\n" + "=" * 70)
    print("测试: get_latest_logs() 函数")
    print("=" * 70)

    try:
        # 调用函数
        print("\n📞 调用 get_latest_logs()...")
        data = get_latest_logs()

        # 检查返回数据结构
        print("\n✅ 函数调用成功!")
        print(f"📦 返回数据类型: {type(data)}")
        print(f"📋 数据键: {list(data.keys())}")

        # 检查中国区数据
        print("\n" + "-" * 70)
        print("🇨🇳 中国区数据检查")
        print("-" * 70)

        if data['cn'] is None:
            print("⚠️  中国区数据为空")
        else:
            print(f"✅ 中国区数据存在")
            print(f"   数据类型: {type(data['cn'])}")
            print(f"   包含字段: {list(data['cn'].keys())}")
            print(f"\n   execution_id: {data['cn']['execution_id']}")
            print(f"   类型: {type(data['cn']['execution_id'])}")
            print(f"\n   timestamp: {data['cn']['timestamp']}")
            print(f"   类型: {type(data['cn']['timestamp'])}")
            print(f"\n   logs: {len(data['cn']['logs'])} 条")
            print(f"   类型: {type(data['cn']['logs'])}")

            if data['cn']['logs']:
                print(f"\n   第一条日志:")
                first_log = data['cn']['logs'][0]
                print(f"      类型: {type(first_log)}")
                print(f"      长度: {len(first_log)}")
                print(f"      时间: {first_log[0]}")
                print(f"      消息: {first_log[1][:60]}...")

        # 检查日本区数据
        print("\n" + "-" * 70)
        print("🇯🇵 日本区数据检查")
        print("-" * 70)

        if data['jp'] is None:
            print("⚠️  日本区数据为空")
        else:
            print(f"✅ 日本区数据存在")
            print(f"   数据类型: {type(data['jp'])}")
            print(f"   包含字段: {list(data['jp'].keys())}")
            print(f"\n   execution_id: {data['jp']['execution_id']}")
            print(f"   类型: {type(data['jp']['execution_id'])}")
            print(f"\n   timestamp: {data['jp']['timestamp']}")
            print(f"   类型: {type(data['jp']['timestamp'])}")
            print(f"\n   logs: {len(data['jp']['logs'])} 条")
            print(f"   类型: {type(data['jp']['logs'])}")

            if data['jp']['logs']:
                print(f"\n   第一条日志:")
                first_log = data['jp']['logs'][0]
                print(f"      类型: {type(first_log)}")
                print(f"      长度: {len(first_log)}")
                print(f"      时间: {first_log[0]}")
                print(f"      消息: {first_log[1][:60]}...")

        # 数据验证
        print("\n" + "=" * 70)
        print("📊 数据验证")
        print("=" * 70)

        validation_passed = True

        # 验证1: 至少有一个区域有数据
        if data['cn'] is None and data['jp'] is None:
            print("❌ 验证失败: 两个区域都没有数据")
            validation_passed = False
        else:
            print("✅ 验证通过: 至少有一个区域有数据")

        # 验证2: 中国区数据结构
        if data['cn']:
            if 'execution_id' in data['cn'] and 'timestamp' in data['cn'] and 'logs' in data['cn']:
                print("✅ 验证通过: 中国区数据结构正确")
            else:
                print("❌ 验证失败: 中国区数据结构不完整")
                validation_passed = False

            if isinstance(data['cn']['logs'], (list, tuple)):
                print("✅ 验证通过: 中国区 logs 是列表/元组")
            else:
                print("❌ 验证失败: 中国区 logs 类型错误")
                validation_passed = False

        # 验证3: 日本区数据结构
        if data['jp']:
            if 'execution_id' in data['jp'] and 'timestamp' in data['jp'] and 'logs' in data['jp']:
                print("✅ 验证通过: 日本区数据结构正确")
            else:
                print("❌ 验证失败: 日本区数据结构不完整")
                validation_passed = False

            if isinstance(data['jp']['logs'], (list, tuple)):
                print("✅ 验证通过: 日本区 logs 是列表/元组")
            else:
                print("❌ 验证失败: 日本区 logs 类型错误")
                validation_passed = False

        # 显示日志内容样例
        print("\n" + "=" * 70)
        print("📝 日志内容样例")
        print("=" * 70)

        if data['cn'] and data['cn']['logs']:
            print("\n🇨🇳 中国区日志 (前3条):")
            for i, log in enumerate(data['cn']['logs'][:3], 1):
                timestamp, message = log
                short_msg = message[:60] + '...' if len(message) > 60 else message
                print(f"   {i}. [{timestamp}] {short_msg}")

        if data['jp'] and data['jp']['logs']:
            print("\n🇯🇵 日本区日志 (前3条):")
            for i, log in enumerate(data['jp']['logs'][:3], 1):
                timestamp, message = log
                short_msg = message[:60] + '...' if len(message) > 60 else message
                print(f"   {i}. [{timestamp}] {short_msg}")

        # 测试结果
        print("\n" + "=" * 70)
        if validation_passed:
            print("🎉 测试通过! db_query 模块工作正常!")
        else:
            print("❌ 测试失败! 请检查数据结构")
        print("=" * 70 + "\n")

        return validation_passed, data

    except Exception as e:
        print(f"\n❌ 测试失败!")
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_data_usage():
    """测试如何使用返回的数据"""
    print("\n" + "=" * 70)
    print("演示: 如何使用返回的数据")
    print("=" * 70)

    data = get_latest_logs()

    print("\n💡 示例1: 检查是否有数据")
    print("-" * 70)
    print("""
if data['cn']:
    print("中国区有数据")
if data['jp']:
    print("日本区有数据")
    """)

    if data['cn']:
        print("✅ 中国区有数据")
    if data['jp']:
        print("✅ 日本区有数据")

    print("\n💡 示例2: 访问 execution_id")
    print("-" * 70)
    print("""
cn_exec_id = data['cn']['execution_id']
jp_exec_id = data['jp']['execution_id']
    """)

    if data['cn']:
        print(f"cn_exec_id = '{data['cn']['execution_id']}'")
    if data['jp']:
        print(f"jp_exec_id = '{data['jp']['execution_id']}'")

    print("\n💡 示例3: 遍历日志")
    print("-" * 70)
    print("""
for timestamp, message in data['cn']['logs']:
    print(f"[{timestamp}] {message}")
    """)

    if data['cn'] and data['cn']['logs']:
        print("\n实际运行结果 (只显示前2条):")
        for timestamp, message in data['cn']['logs'][:2]:
            short_msg = message[:50] + '...' if len(message) > 50 else message
            print(f"[{timestamp}] {short_msg}")

    print("\n💡 示例4: 统计日志数量")
    print("-" * 70)
    print("""
cn_count = len(data['cn']['logs']) if data['cn'] else 0
jp_count = len(data['jp']['logs']) if data['jp'] else 0
total = cn_count + jp_count
    """)

    cn_count = len(data['cn']['logs']) if data['cn'] else 0
    jp_count = len(data['jp']['logs']) if data['jp'] else 0
    total = cn_count + jp_count

    print(f"cn_count = {cn_count}")
    print(f"jp_count = {jp_count}")
    print(f"total = {total}")

    print("\n" + "=" * 70)
    print("✅ 使用示例演示完成")
    print("=" * 70 + "\n")


def main():
    """主测试函数"""
    print("\n" + "🧪 " + "=" * 66)
    print("🧪 测试 db_query 模块")
    print("🧪 " + "=" * 66)

    # 测试1: 基本功能测试
    success, data = test_get_latest_logs()

    if not success:
        print("\n⚠️  基本功能测试失败,跳过后续测试")
        return False

    # 测试2: 数据使用示例
    test_data_usage()

    # 总结
    print("\n" + "=" * 70)
    print("🎯 测试总结")
    print("=" * 70)
    print("""
✅ get_latest_logs() 函数测试通过

📌 返回数据结构:
{
    'cn': {
        'execution_id': str,      # 执行ID
        'timestamp': datetime,    # 最新时间
        'logs': [(timestamp, message), ...]  # 日志列表
    },
    'jp': { ... }  # 相同结构
}

📌 使用方法:
1. data = get_latest_logs()
2. 检查: if data['cn']
3. 访问: data['cn']['execution_id']
4. 遍历: for timestamp, message in data['cn']['logs']

📌 下一步:
现在可以开始开发 AI 处理模块了!
AI 模块将接收这个 data 字典作为输入。
    """)
    print("=" * 70 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)