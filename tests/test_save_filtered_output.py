# tests/test_save_filtered_output.py
"""
保存过滤后的数据到文件,方便查看将要发送给 AI 的内容
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.db_query import get_latest_logs
from modules.log_filter import filter_logs
from datetime import datetime


def format_for_ai(filtered_data):
    """
    将过滤后的数据格式化为将要发送给 AI 的文本格式

    Args:
        filtered_data: 过滤后的数据

    Returns:
        格式化的文本字符串
    """
    output = []

    # 中国区
    if filtered_data['cn']:
        cn = filtered_data['cn']

        output.append("【中国区 (arkcn)】")
        output.append(f"执行ID: {cn['execution_id']}")
        output.append(f"开始时间: {cn['start_time']}")
        output.append(f"结束时间: {cn['end_time']}")
        output.append(f"日志条数: {len(cn['logs'])} 条")
        output.append("")
        output.append("执行日志:")

        for message in cn['logs']:
            output.append(message)

        output.append("")

    # 日本区
    if filtered_data['jp']:
        jp = filtered_data['jp']

        output.append("【日本区 (arkjp)】")
        output.append(f"执行ID: {jp['execution_id']}")
        output.append(f"开始时间: {jp['start_time']}")
        output.append(f"结束时间: {jp['end_time']}")
        output.append(f"日志条数: {len(jp['logs'])} 条")
        output.append("")
        output.append("执行日志:")

        for message in jp['logs']:
            output.append(message)

        output.append("")

    return "\n".join(output)


def save_filtered_output():
    """
    保存过滤后的输出到文件
    """
    print("\n" + "=" * 80)
    print("💾 保存过滤后的数据到文件")
    print("=" * 80)

    # 读取并过滤数据
    print("\n📖 读取原始数据...")
    raw_data = get_latest_logs()

    print("🔄 过滤数据...")
    filtered_data = filter_logs(raw_data)

    # 格式化为 AI 输入格式
    print("📝 格式化为 AI 输入格式...")
    ai_input = format_for_ai(filtered_data)

    # 保存到文件
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_input_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ai_input)

    print(f"\n✅ 文件已保存到: {filepath}")

    # 统计信息
    lines = ai_input.split('\n')
    chars = len(ai_input)

    print("\n" + "=" * 80)
    print("📊 文件统计")
    print("=" * 80)
    print(f"文件路径: {filepath}")
    print(f"总行数: {len(lines)} 行")
    print(f"总字符数: {chars} 字符")

    if filtered_data['cn']:
        print(f"\n🇨🇳 中国区: {len(filtered_data['cn']['logs'])} 条日志")

    if filtered_data['jp']:
        print(f"🇯🇵 日本区: {len(filtered_data['jp']['logs'])} 条日志")

    # 显示文件内容预览
    print("\n" + "=" * 80)
    print("📄 文件内容预览 (前30行)")
    print("=" * 80)
    for i, line in enumerate(lines[:30], 1):
        print(line)

    if len(lines) > 30:
        print(f"\n... (还有 {len(lines) - 30} 行)")

    print("\n" + "=" * 80)
    print("💡 提示:")
    print(f"   - 完整内容已保存到: {filepath}")
    print("   - 可以用文本编辑器打开查看")
    print("   - 这就是将要发送给 AI 的内容")
    print("=" * 80 + "\n")

    return filepath, ai_input


def main():
    """主函数"""
    print("\n" + "🚀 " + "=" * 76)
    print("🚀 生成 AI 输入文件测试")
    print("🚀 " + "=" * 76)

    filepath, content = save_filtered_output()

    print("\n" + "=" * 80)
    print("✅ 测试完成!")
    print("\n下一步:")
    print("1. 打开文件查看内容")
    print(f"   文件路径: {filepath}")
    print("2. 确认这就是你想发送给 AI 的格式")
    print("3. 如果格式没问题,就可以开始开发 AI 模块了")
    print("=" * 80 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)