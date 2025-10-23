# tests/test_read_latest.py
"""
简单测试: 读取两个表的最新数据
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pymysql
from config.database import DB_CONFIG


def test_read_latest():
    """读取并显示最新数据"""
    print("\n" + "=" * 70)
    print("测试: 读取 arkcn_logs 和 arkjp_logs 最新数据")
    print("=" * 70)

    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("\n✅ 数据库连接成功!")

        # ===== 测试1: 读取 arkcn_logs 最新数据 =====
        print("\n" + "-" * 70)
        print("🇨🇳 中国区 (arkcn_logs)")
        print("-" * 70)

        # 1.1 获取最新的 execution_id
        cursor.execute("""
            SELECT execution_id, MAX(timestamp) as latest_time
            FROM arkcn_logs
            GROUP BY execution_id
            ORDER BY latest_time DESC
            LIMIT 1
        """)
        cn_result = cursor.fetchone()

        if cn_result:
            cn_exec_id, cn_time = cn_result
            print(f"\n📌 最新 execution_id: {cn_exec_id}")
            print(f"📅 最新时间: {cn_time}")

            # 1.2 获取该 execution_id 的所有日志
            cursor.execute("""
                SELECT id, execution_id, timestamp, log_message
                FROM arkcn_logs
                WHERE execution_id = %s
                ORDER BY timestamp ASC
            """, (cn_exec_id,))
            cn_logs = cursor.fetchall()

            print(f"📊 日志总数: {len(cn_logs)} 条")

            # 显示前5条日志
            print(f"\n📋 前5条日志:")
            for i, log in enumerate(cn_logs[:5], 1):
                log_id, exec_id, timestamp, message = log
                # 限制消息长度
                short_msg = message[:60] + '...' if len(message) > 60 else message
                print(f"  {i}. [{timestamp}] {short_msg}")

            if len(cn_logs) > 5:
                print(f"\n  ... (省略中间 {len(cn_logs) - 10} 条)")

                # 显示后5条日志
                print(f"\n📋 后5条日志:")
                for i, log in enumerate(cn_logs[-5:], len(cn_logs) - 4):
                    log_id, exec_id, timestamp, message = log
                    short_msg = message[:60] + '...' if len(message) > 60 else message
                    print(f"  {i}. [{timestamp}] {short_msg}")
        else:
            print("⚠️  未找到数据")

        # ===== 测试2: 读取 arkjp_logs 最新数据 =====
        print("\n" + "-" * 70)
        print("🇯🇵 日本区 (arkjp_logs)")
        print("-" * 70)

        # 2.1 获取最新的 execution_id
        cursor.execute("""
            SELECT execution_id, MAX(timestamp) as latest_time
            FROM arkjp_logs
            GROUP BY execution_id
            ORDER BY latest_time DESC
            LIMIT 1
        """)
        jp_result = cursor.fetchone()

        if jp_result:
            jp_exec_id, jp_time = jp_result
            print(f"\n📌 最新 execution_id: {jp_exec_id}")
            print(f"📅 最新时间: {jp_time}")

            # 2.2 获取该 execution_id 的所有日志
            cursor.execute("""
                SELECT id, execution_id, timestamp, log_message
                FROM arkjp_logs
                WHERE execution_id = %s
                ORDER BY timestamp ASC
            """, (jp_exec_id,))
            jp_logs = cursor.fetchall()

            print(f"📊 日志总数: {len(jp_logs)} 条")

            # 显示前5条日志
            print(f"\n📋 前5条日志:")
            for i, log in enumerate(jp_logs[:5], 1):
                log_id, exec_id, timestamp, message = log
                short_msg = message[:60] + '...' if len(message) > 60 else message
                print(f"  {i}. [{timestamp}] {short_msg}")

            if len(jp_logs) > 5:
                print(f"\n  ... (省略中间 {len(jp_logs) - 10} 条)")

                # 显示后5条日志
                print(f"\n📋 后5条日志:")
                for i, log in enumerate(jp_logs[-5:], len(jp_logs) - 4):
                    log_id, exec_id, timestamp, message = log
                    short_msg = message[:60] + '...' if len(message) > 60 else message
                    print(f"  {i}. [{timestamp}] {short_msg}")
        else:
            print("⚠️  未找到数据")

        # ===== 总结 =====
        print("\n" + "=" * 70)
        print("📊 数据读取总结")
        print("=" * 70)

        if cn_result and jp_result:
            print(f"\n✅ 成功读取两个区域的最新数据:")
            print(f"   🇨🇳 中国区: {len(cn_logs)} 条日志 (execution_id: {cn_exec_id})")
            print(f"   🇯🇵 日本区: {len(jp_logs)} 条日志 (execution_id: {jp_exec_id})")
            print(f"   📈 总计: {len(cn_logs) + len(jp_logs)} 条日志")
            print(f"\n✨ 数据读取正确! 可以继续开发 AI 模块!")
        else:
            print("\n⚠️  部分数据读取失败")

        print("=" * 70 + "\n")

        # 关闭连接
        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🚀 开始测试数据读取...\n")
    success = test_read_latest()

    if success:
        print("✅ 测试完成!")
    else:
        print("❌ 测试失败!")

    sys.exit(0 if success else 1)