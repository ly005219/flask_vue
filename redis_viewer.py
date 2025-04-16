import sys
import os
import pickle
import json
import redis
from functools import wraps

# 序列化和反序列化工具函数
def serialize_data(data):
    """将数据序列化为二进制格式，支持复杂Python对象"""
    try:
        return pickle.dumps(data)
    except Exception as e:
        print(f"序列化错误: {e}")
        return None

def deserialize_data(data):
    """将二进制数据反序列化为Python对象"""
    if data is None:
        return None
    try:
        return pickle.loads(data)
    except Exception as e:
        print(f"反序列化错误: {e}")
        return None

# 连接到Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def view_all_keys():
    """查看所有键"""
    keys = r.keys('*')
    print("所有键:")
    for key in keys:
        try:
            key_str = key.decode('utf-8')
            print(f"- {key_str}")
        except:
            print(f"- {key} (无法解码)")

def view_role_list():
    """查看角色列表缓存"""
    role_data = r.get('roles_list')
    if role_data:
        try:
            roles = deserialize_data(role_data)
            print("\n角色列表数据:")
            print(json.dumps(roles, ensure_ascii=False, indent=2))  # 美化输出
        except Exception as e:
            print(f"无法反序列化数据: {e}")
    else:
        print("\n未找到角色列表缓存")

def view_role_menus(role_id):
    """查看特定角色的菜单缓存"""
    key = f'role_menus:{role_id}'
    role_menu_data = r.get(key)
    if role_menu_data:
        try:
            menus = deserialize_data(role_menu_data)
            print(f"\n角色ID {role_id} 的菜单数据:")
            print(json.dumps(menus, ensure_ascii=False, indent=2))  # 美化输出
        except Exception as e:
            print(f"无法反序列化数据: {e}")
    else:
        print(f"\n未找到角色 {role_id} 的菜单缓存")

def view_menu_data():
    """查看菜单缓存"""
    menu_data = r.get('menus')
    if menu_data:
        try:
            menus = deserialize_data(menu_data)
            print("\n菜单数据:")
            print(json.dumps(menus, ensure_ascii=False, indent=2))  # 美化输出
        except Exception as e:
            print(f"无法反序列化数据: {e}")
    else:
        print("\n未找到菜单缓存")

class RedisClient:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            # 使用环境变量或配置文件中的值
            host = os.environ.get('REDIS_HOST', 'localhost')
            port = int(os.environ.get('REDIS_PORT', 6379))
            db = int(os.environ.get('REDIS_DB', 0))
            password = os.environ.get('REDIS_PASSWORD', None)
            
            cls._instance = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=False
            )
            print(f"Connected to Redis at {host}:{port}, db={db}")
        return cls._instance

# 测试Redis连接和序列化
def test_redis_connection():
    print("\n===== 测试Redis连接和序列化 =====")
    test_data = {
        'name': '测试数据',
        'value': 123,
        'list': [1, 2, 3],
        'dict': {'a': 1, 'b': 2}
    }
    
    # 测试序列化和存储
    serialized = serialize_data(test_data)
    r.set('test_key', serialized)
    print("测试数据已存储")
    
    # 测试获取和反序列化
    retrieved = r.get('test_key')
    deserialized = deserialize_data(retrieved)
    print("\n获取的测试数据:")
    print(json.dumps(deserialized, ensure_ascii=False, indent=2))
    
    # 清理测试数据
    r.delete('test_key')
    print("\n测试完成，数据已清理")

if __name__ == "__main__":
    print("===== Redis缓存查看器 =====")
    # 查看所有键
    view_all_keys()
    
    # 查看角色列表
    view_role_list()
    
    # 查看角色菜单
    role_id = 1  # 替换为您想查看的角色ID
    view_role_menus(role_id)
    
    # 查看菜单数据
    view_menu_data()
    
    # 运行测试
    test_redis_connection() 