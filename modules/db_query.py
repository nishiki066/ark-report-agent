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


# 原函数名：create_or_update_ai_report_placeholder
# 新函数名：create_ai_report_placeholder

def create_ai_report_placeholder(arkcn_execution_id, arkjp_execution_id, balance_data):
    """
    创建 AI 报告占位记录（每次都插入新记录）

    优先选择 CNY 币种的余额信息

    Args:
        arkcn_execution_id: 中国区执行ID
        arkjp_execution_id: 日本区执行ID
        balance_data: check_balance() 返回的余额数据

    Returns:
        int: report_id（新插入记录的ID）
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # 解析余额数据
        is_available = balance_data.get('is_available', True)
        balance_infos = balance_data.get('balance_infos', [])

        if balance_infos:
            # 优先查找 CNY 币种
            balance_info = None
            for info in balance_infos:
                if info.get('currency') == 'CNY':
                    balance_info = info
                    print(f"   ✅ 使用 CNY 币种余额")
                    break

            # 如果没找到 CNY，使用第一个币种
            if not balance_info:
                balance_info = balance_infos[0]
                print(f"   ⚠️  未找到 CNY 币种，使用 {balance_info.get('currency', 'UNKNOWN')} 币种")

            currency = balance_info.get('currency', 'CNY')
            total_balance = float(balance_info.get('total_balance', '0.00'))
            granted_balance = float(balance_info.get('granted_balance', '0.00'))
            topped_up_balance = float(balance_info.get('topped_up_balance', '0.00'))
        else:
            # 如果 balance_infos 为空，使用默认值
            print(f"   ⚠️  balance_infos 为空，使用默认值")
            currency = 'CNY'
            total_balance = 0.00
            granted_balance = 0.00
            topped_up_balance = 0.00

        # 直接插入新记录
        sql = """
            INSERT INTO ai_reports (
                arkcn_execution_id,
                arkjp_execution_id,
                report_content,
                status,
                api_is_available,
                api_currency,
                api_total_balance,
                api_granted_balance,
                api_topped_up_balance
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            arkcn_execution_id,
            arkjp_execution_id,
            '',  # report_content 初始为空
            'generating',  # status 初始为 generating
            is_available,
            currency,
            total_balance,
            granted_balance,
            topped_up_balance
        )

        cursor.execute(sql, values)
        conn.commit()

        # 获取新插入记录的 ID
        report_id = cursor.lastrowid

        return report_id

    finally:
        cursor.close()
        conn.close()

# update_ai_report 函数保持不变
def update_ai_report(report_id, report_content, status='completed'):
    """
    更新 AI 报告的内容和状态

    Args:
        report_id: 报告记录ID
        report_content: AI 生成的报告内容（或错误信息）
        status: 报告状态

    Returns:
        bool: 更新是否成功
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        sql = """
            UPDATE ai_reports
            SET report_content = %s,
                status = %s
            WHERE id = %s
        """

        cursor.execute(sql, (report_content, status, report_id))
        conn.commit()

        return cursor.rowcount > 0

    finally:
        cursor.close()
        conn.close()