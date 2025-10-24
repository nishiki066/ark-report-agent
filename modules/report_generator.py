# modules/report_generator.py
"""
报告生成器模块 - 整合完整的 AI 报告生成流程
"""
from .db_query import (
    get_latest_logs,
    create_ai_report_placeholder,
    update_ai_report
)
from .log_filter import filter_logs
from .ai_processor import process_with_ai, check_balance


def generate_ai_report(stream=True):
    """
    生成 AI 报告 - 完整流程

    流程步骤：
    1. 查询最新日志
    2. 查询 API 余额
    3. 创建/更新报告占位记录
    4. 过滤和格式化日志
    5. 生成 AI 报告（带异常处理）
    6. 更新报告内容和状态
    7. 完成

    Args:
        stream: 是否使用流式输出（默认 True）

    Returns:
        dict: {
            'success': bool,           # 是否成功
            'report_id': int,          # 报告ID
            'report_content': str,     # 报告内容（或错误信息）
            'status': str,             # 状态：completed/failed
            'arkcn_execution_id': str, # 中国区执行ID
            'arkjp_execution_id': str  # 日本区执行ID
        }
    """

    print("\n" + "=" * 80)
    print("🚀 开始生成 AI 报告")
    print("=" * 80)

    report_id = None
    arkcn_id = None
    arkjp_id = None

    try:
        # ============================================================
        # 步骤1：查询最新日志
        # ============================================================
        print("\n📋 步骤1：查询最新日志...")
        logs_data = get_latest_logs()

        if not logs_data['cn'] or not logs_data['jp']:
            raise Exception("未找到日志数据，请确认数据库中有执行记录")

        arkcn_id = logs_data['cn']['execution_id']
        arkjp_id = logs_data['jp']['execution_id']

        print(f"   ✅ 中国区 execution_id: {arkcn_id}")
        print(f"   ✅ 日本区 execution_id: {arkjp_id}")

        # ============================================================
        # 步骤2：查询 API 余额
        # ============================================================
        print("\n💰 步骤2：查询 API 余额...")
        balance_data = check_balance(show_detail=False)

        if balance_data.get('balance_infos'):
            balance_info = balance_data['balance_infos'][0]
            print(f"   ✅ 当前余额: {balance_info.get('total_balance', '0.00')} {balance_info.get('currency', 'CNY')}")
        else:
            print("   ⚠️  未获取到余额信息，使用默认值")

        # ============================================================
        # 步骤3：创建/更新报告占位记录
        # ============================================================
        print("\n📝 步骤3：创建报告占位记录...")
        report_id = create_ai_report_placeholder(
            arkcn_id,
            arkjp_id,
            balance_data
        )

        if report_id:
            print(f"   ✅ 报告记录已创建/更新，report_id: {report_id}")
        else:
            raise Exception("创建报告占位记录失败")

        # ============================================================
        # 步骤4：过滤和格式化日志
        # ============================================================
        print("\n🔍 步骤4：过滤和格式化日志...")
        filtered_data = filter_logs(logs_data)

        cn_log_count = len(filtered_data['cn']['logs']) if filtered_data['cn'] else 0
        jp_log_count = len(filtered_data['jp']['logs']) if filtered_data['jp'] else 0

        print(f"   ✅ 中国区日志: {cn_log_count} 条")
        print(f"   ✅ 日本区日志: {jp_log_count} 条")

        # ============================================================
        # 步骤5：生成 AI 报告
        # ============================================================
        print("\n🤖 步骤5：生成 AI 报告...")
        print("-" * 80)

        report_content = process_with_ai(filtered_data, stream=stream)

        print("-" * 80)
        print("   ✅ AI 报告生成完成")

        # ============================================================
        # 步骤6：更新报告内容 - 成功
        # ============================================================
        print("\n💾 步骤6：保存报告到数据库...")
        success = update_ai_report(report_id, report_content, status='completed')

        if success:
            print("   ✅ 报告已保存")
        else:
            print("   ⚠️  保存报告失败")

        # ============================================================
        # 步骤7：完成
        # ============================================================
        print("\n" + "=" * 80)
        print("✅ AI 报告生成成功！")
        print("=" * 80)
        print(f"   报告ID: {report_id}")
        print(f"   中国区: {arkcn_id}")
        print(f"   日本区: {arkjp_id}")
        print(f"   状态: completed")
        print("=" * 80 + "\n")

        return {
            'success': True,
            'report_id': report_id,
            'report_content': report_content,
            'status': 'completed',
            'arkcn_execution_id': arkcn_id,
            'arkjp_execution_id': arkjp_id
        }

    except Exception as e:
        # ============================================================
        # 异常处理：更新报告状态为失败
        # ============================================================
        error_message = f"生成报告失败: {str(e)}"
        print(f"\n❌ 错误: {error_message}")

        # 如果已创建占位记录，更新为失败状态
        if report_id:
            print("\n💾 更新报告状态为失败...")
            update_ai_report(report_id, error_message, status='failed')
            print("   ✅ 失败状态已记录")

        print("\n" + "=" * 80)
        print("❌ AI 报告生成失败")
        print("=" * 80)
        print(f"   错误信息: {str(e)}")
        if report_id:
            print(f"   报告ID: {report_id}")
        if arkcn_id:
            print(f"   中国区: {arkcn_id}")
        if arkjp_id:
            print(f"   日本区: {arkjp_id}")
        print("=" * 80 + "\n")

        return {
            'success': False,
            'report_id': report_id,
            'report_content': error_message,
            'status': 'failed',
            'arkcn_execution_id': arkcn_id,
            'arkjp_execution_id': arkjp_id
        }