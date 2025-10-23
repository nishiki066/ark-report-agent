# tests/test_view_full_data.py
"""
查看完整的日志数据,为后续 AI 分析做准备
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pymysql
from config.database import DB_CONFIG


def view_full_logs(table_name, region_name, emoji):
    """查看指定表的完整日志"""
    print("\n" + "=" * 80)
    print(f"{emoji} {region_name} ({table_name}) - 完整日志数据")
    print("=" * 80)

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 获取最新的 execution_id
        cursor.execute(f"""
            SELECT execution_id, MAX(timestamp) as latest_time
            FROM {table_name}
            GROUP BY execution_id
            ORDER BY latest_time DESC
            LIMIT 1
        """)
        result = cursor.fetchone()

        if not result:
            print(f"⚠️  {table_name} 中没有数据")
            return None

        execution_id, latest_time = result

        print(f"\n📋 基本信息:")
        print(f"   execution_id: {execution_id}")
        print(f"   最新时间: {latest_time}")

        # 获取所有日志
        cursor.execute(f"""
            SELECT id, execution_id, timestamp, log_message
            FROM {table_name}
            WHERE execution_id = %s
            ORDER BY timestamp ASC
        """, (execution_id,))
        logs = cursor.fetchall()

        print(f"   日志总数: {len(logs)} 条")

        # 显示所有日志
        print(f"\n📝 完整日志内容:\n")
        print("-" * 80)

        for i, log in enumerate(logs, 1):
            log_id, exec_id, timestamp, message = log
            print(f"{i:3d}. [{timestamp}] {message}")

        print("-" * 80)

        # 简单分析
        print(f"\n📊 简单分析:")

        # 统计关键词
        error_count = sum(
            1 for log in logs if any(word in log[3].lower() for word in ['error', '错误', 'failed', '失败']))
        success_count = sum(
            1 for log in logs if any(word in log[3].lower() for word in ['success', '成功', 'completed', '完成']))

        print(f"   错误相关日志: {error_count} 条")
        print(f"   成功相关日志: {success_count} 条")

        # 判断执行状态
        last_message = logs[-1][3].lower() if logs else ""
        if 'error' in last_message or '错误' in last_message:
            status = "❌ 执行失败"
        elif 'completed' in last_message or '完成' in last_message:
            status = "✅ 执行成功"
        else:
            status = "⚪ 状态未知"

        print(f"   执行状态: {status}")

        # 提取关键信息
        print(f"\n🔍 关键信息:")
        for log in logs:
            message = log[3]
            # 查找关键信息
            if 'ssh连接失败' in message.lower() or 'connection' in message.lower():
                print(f"   ⚠️  连接问题: {message}")
            elif 'maa' in message.lower() or 'mumu' in message.lower():
                print(f"   🎮 游戏相关: {message}")
            elif '完成' in message or 'completed' in message.lower():
                print(f"   ✅ 完成标记: {message}")

        cursor.close()
        conn.close()

        return {
            'execution_id': execution_id,
            'timestamp': latest_time,
            'logs': logs,
            'log_count': len(logs),
            'error_count': error_count,
            'success_count': success_count
        }

    except Exception as e:
        print(f"❌ 读取失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("\n" + "🔍 " + "=" * 76)
    print("🔍 查看完整日志数据")
    print("🔍 " + "=" * 76)

    # 读取中国区数据
    cn_data = view_full_logs('arkcn_logs', '中国区', '🇨🇳')

    # 读取日本区数据
    jp_data = view_full_logs('arkjp_logs', '日本区', '🇯🇵')

    # 总结
    print("\n" + "=" * 80)
    print("📊 数据总览")
    print("=" * 80)

    if cn_data and jp_data:
        print(f"\n✅ 成功读取两个区域的数据:")
        print(f"\n🇨🇳 中国区:")
        print(f"   execution_id: {cn_data['execution_id']}")
        print(f"   日志数量: {cn_data['log_count']} 条")
        print(f"   错误数量: {cn_data['error_count']} 条")
        print(f"   成功标识: {cn_data['success_count']} 条")

        print(f"\n🇯🇵 日本区:")
        print(f"   execution_id: {jp_data['execution_id']}")
        print(f"   日志数量: {jp_data['log_count']} 条")
        print(f"   错误数量: {jp_data['error_count']} 条")
        print(f"   成功标识: {jp_data['success_count']} 条")

        print(f"\n📈 总计: {cn_data['log_count'] + jp_data['log_count']} 条日志")

        # 下一步建议
        print("\n" + "=" * 80)
        print("💡 下一步操作建议")
        print("=" * 80)
        print("""
现在我们已经看到完整的日志数据,可以考虑:

1. 数据过滤:
   - 过滤掉哪些不重要的日志?
   - 保留哪些关键信息?

2. AI 分析重点:
   - 执行是否成功?
   - 遇到了什么问题?
   - 关键操作是否完成?
   - 耗时分析?

3. 报告格式:
   - 需要包含哪些内容?
   - 如何呈现给用户?
        """)
        print("=" * 80 + "\n")

    return cn_data, jp_data


if __name__ == "__main__":
    cn_data, jp_data = main()