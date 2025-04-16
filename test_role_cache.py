import sys
import os
import time
import json
import traceback
import redis

# 直接测试Redis连接
def test_redis_connection():
    """测试Redis连接和缓存功能"""
    try:
        print("开始测试Redis连接...")
        
        # 连接Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # 测试连接
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        print(f"连接测试: {'成功' if value == b'test_value' else '失败'}")
        
        # 检查现有的键
        print("\n当前Redis中的所有键:")
        keys = r.keys('*')
        for key in keys:
            try:
                key_str = key.decode('utf-8')
                print(f"- {key_str}")
            except:
                print(f"- {key} (无法解码)")
        
        # 清除测试键
        r.delete('test_key')
        
        # 测试redis_viewer.py中的功能
        try:
            from redis_viewer import serialize_data, deserialize_data
            
            # 测试序列化和反序列化
            print("\n测试序列化和反序列化功能...")
            test_data = {'name': '测试数据', 'status': 200, 'data': [1, 2, 3]}
            
            serialized = serialize_data(test_data)
            r.set('test_key2', serialized)
            
            retrieved = r.get('test_key2')
            deserialized = deserialize_data(retrieved)
            
            print(f"原始数据: {test_data}")
            print(f"反序列化数据: {deserialized}")
            print(f"数据匹配: {test_data == deserialized}")
            
            # 清除测试键
            r.delete('test_key2')
        except ImportError:
            print("\n无法导入redis_viewer.py中的功能，跳过序列化测试")
        
        print("\n测试完成!")
        
    except Exception as e:
        print(f"测试Redis连接时出错: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_redis_connection() 