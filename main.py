# main.py
"""
AI 报告生成系统 - 主程序入口

功能：
1. 自动获取最新的日志执行记录
2. 调用 DeepSeek AI 分析日志
3. 生成结构化的执行报告
4. 保存到数据库
"""
from modules import generate_ai_report


def main():
    """主程序入口"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "AI 报告生成系统" + " " * 43 + "║")
    print("╚" + "=" * 78 + "╝")

    try:
        # 生成报告（使用流式输出）
        result = generate_ai_report(stream=True)

        # 根据结果决定退出码
        if result['success']:
            print("\n✅ 程序执行成功")
            return 0
        else:
            print("\n⚠️  程序执行完成，但报告生成失败")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
        return 2

    except Exception as e:
        print(f"\n\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        return 3


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)