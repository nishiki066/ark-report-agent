# tests/test_config.py
"""
测试配置文件是否正确加载
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import DB_CONFIG, AI_CONFIG, APP_CONFIG, print_config_info, validate_config


def test_env_file_exists():
    """检查 .env 文件是否存在"""
    print("\n" + "=" * 60)
    print("测试 1: 检查 .env 文件")
    print("=" * 60)

    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

    if os.path.exists(env_path):
        print(f"✅ .env 文件存在: {os.path.abspath(env_path)}")
        return True
    else:
        print(f"⚠️  .env 文件不存在: {os.path.abspath(env_path)}")
        print("提示: 请从 .env.example 复制并修改")
        return False


def test_config_values():
    """检查配置值是否有效"""
    print("\n" + "=" * 60)
    print("测试 2: 检查配置值")
    print("=" * 60)

    issues = []

    # 检查数据库配置
    if not DB_CONFIG['host']:
        issues.append("DB_HOST 未设置")
    if not DB_CONFIG['user']:
        issues.append("DB_USER 未设置")
    if not DB_CONFIG['password']:
        issues.append("DB_PASSWORD 未设置")
    if not DB_CONFIG['database']:
        issues.append("DB_NAME 未设置")

    if issues:
        print("❌ 发现配置问题:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ 数据库配置完整")
        return True


def test_config_validation():
    """运行配置验证"""
    print("\n" + "=" * 60)
    print("测试 3: 配置验证")
    print("=" * 60)

    result = validate_config()

    if result:
        print("✅ 配置验证通过")
    else:
        print("❌ 配置验证失败")

    return result


if __name__ == "__main__":
    print("\n🔍 开始配置测试...\n")

    # 先显示配置信息
    print_config_info()

    # 运行测试
    test1 = test_env_file_exists()
    test2 = test_config_values()
    test3 = test_config_validation()

    # 总结
    print("\n" + "=" * 60)
    print("配置测试总结")
    print("=" * 60)
    print(f".env 文件检查: {'✅ 通过' if test1 else '❌ 失败'}")
    print(f"配置值检查: {'✅ 通过' if test2 else '❌ 失败'}")
    print(f"配置验证: {'✅ 通过' if test3 else '❌ 失败'}")

    if test1 and test2 and test3:
        print("\n🎉 所有配置测试通过!")
    else:
        print("\n⚠️  部分测试失败,请检查配置")

    print("=" * 60 + "\n")