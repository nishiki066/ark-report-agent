# modules/db_query.py
"""
数据库查询模块 - 只负责读取数据
"""
import pymysql
from config.database import DB_CONFIG


def get_latest_logs():
    """
    获取两个区域的最新日志数据

    Returns:
        dict: {
            'cn': {
                'execution_id': str,
                'timestamp': datetime,
                'logs': list of tuples
            },
            'jp': {
                'execution_id': str,
                'timestamp': datetime,
                'logs': list of tuples
            }
        }
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    result = {
        'cn': None,
        'jp': None
    }

    try:
        # 读取中国区最新数据
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

            cursor.execute("""
                SELECT timestamp, log_message
                FROM arkcn_logs
                WHERE execution_id = %s
                ORDER BY timestamp ASC
            """, (cn_exec_id,))
            cn_logs = cursor.fetchall()

            result['cn'] = {
                'execution_id': cn_exec_id,
                'timestamp': cn_time,
                'logs': cn_logs
            }

        # 读取日本区最新数据
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

            cursor.execute("""
                SELECT timestamp, log_message
                FROM arkjp_logs
                WHERE execution_id = %s
                ORDER BY timestamp ASC
            """, (jp_exec_id,))
            jp_logs = cursor.fetchall()

            result['jp'] = {
                'execution_id': jp_exec_id,
                'timestamp': jp_time,
                'logs': jp_logs
            }

    finally:
        cursor.close()
        conn.close()

    return result


if __name__ == "__main__":
    """测试读取功能"""
    print("\n测试数据读取模块...")

    data = get_latest_logs()

    if data['cn']:
        print(f"\n🇨🇳 中国区:")
        print(f"   execution_id: {data['cn']['execution_id']}")
        print(f"   时间: {data['cn']['timestamp']}")
        print(f"   日志数: {len(data['cn']['logs'])}")

    if data['jp']:
        print(f"\n🇯🇵 日本区:")
        print(f"   execution_id: {data['jp']['execution_id']}")
        print(f"   时间: {data['jp']['timestamp']}")
        print(f"   日志数: {len(data['jp']['logs'])}")

    print("\n✅ 数据读取完成")