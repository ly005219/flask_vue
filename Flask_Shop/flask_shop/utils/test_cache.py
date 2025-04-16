import sys
import os
import time
import threading
import json

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask_shop import create_app
from flask_shop.utils.redis_cache import (
    RedisClient, deserialize_data, serialize_data,
    cache_with_key, clear_cache_by_prefix,
    cache_update_with_delay_double_deletion
)

# 创建测试应用
app = create_app('development')

# 测试函数
def test_cache_functionality():
    """测试缓存的基本功能"""
    with app.app_context():
        # 获取Redis客户端
        redis_client = RedisClient.get_instance()
        
        # 测试数据
        test_data = {'message': '这是测试数据', 'code': 200, 'values': [1, 2, 3]}
        
        # 测试序列化和反序列化
        print("测试序列化和反序列化...")
        serialized = serialize_data(test_data)
        redis_client.set('test_key', serialized, ex=60)  # 60秒过期
        
        retrieved = redis_client.get('test_key')
        deserialized = deserialize_data(retrieved)
        
        print(f"原始数据: {test_data}")
        print(f"反序列化数据: {deserialized}")
        print(f"数据匹配: {test_data == deserialized}")
        
        # 测试缓存键的格式
        print("\n测试缓存键格式...")
        
        # 定义测试类和装饰函数
        class TestClass:
            @cache_with_key("test_prefix", ttl=3600)
            def test_method(self, arg1, arg2, keyword=None):
                return {'arg1': arg1, 'arg2': arg2, 'keyword': keyword}
        
        # 创建实例并调用方法
        instance = TestClass()
        result1 = instance.test_method(1, "test", keyword="value")
        
        # 查找所有测试前缀的键
        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = redis_client.scan(cursor, match="test_prefix*")
            keys.extend([k.decode('utf-8') for k in partial_keys])
            if cursor == 0:
                break
        
        print(f"找到的缓存键: {keys}")
        expected_key = "test_prefix:1:test:keyword=value"
        print(f"期望的键格式: {expected_key}")
        print(f"键格式正确: {expected_key in keys}")
        
        # 测试清除缓存
        print("\n测试清除缓存...")
        count = clear_cache_by_prefix("test_prefix")
        print(f"删除的键数量: {count}")
        
        # 验证键已被删除
        remaining = redis_client.keys("test_prefix*")
        print(f"剩余键数量: {len(remaining)}")
        
        # 测试延迟双删
        print("\n测试延迟双删策略...")
        
        # 添加一些测试键
        for i in range(5):
            redis_client.set(f"delay_test:{i}", serialize_data(f"值 {i}"), ex=3600)
        
        print("添加的测试键:")
        test_keys = redis_client.keys("delay_test*")
        print([k.decode('utf-8') for k in test_keys])
        
        # 定义测试函数
        @cache_update_with_delay_double_deletion(['delay_test'], delay=2.0)
        def update_data():
            print("执行数据库操作...")
            time.sleep(1)  # 模拟数据库操作
            return "操作完成"
        
        # 执行函数，触发延迟双删
        result = update_data()
        print(f"函数返回: {result}")
        
        # 检查第一次删除后的键
        print("\n第一次删除后的键:")
        remaining = redis_client.keys("delay_test*")
        print([k.decode('utf-8') for k in remaining])
        
        # 等待延迟删除完成
        print("\n等待延迟删除完成...")
        time.sleep(3)
        
        # 检查第二次删除后的键
        print("\n第二次删除后的键:")
        remaining = redis_client.keys("delay_test*")
        print([k.decode('utf-8') for k in remaining])
        
        # 清理测试键
        redis_client.delete('test_key')
        
        print("\n测试完成!")

if __name__ == "__main__":
    test_cache_functionality() 