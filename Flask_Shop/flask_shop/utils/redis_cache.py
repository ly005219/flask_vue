import redis
import json
import pickle
from functools import wraps
from flask import current_app
import time
import threading
import os

# Redis连接单例
class RedisClient:
    _instance = None
    
    #用于docker连接的时候开启
    # @classmethod
    # def get_instance(cls):
    #     if cls._instance is None:
    #         # 从环境变量中获取Redis主机名，默认为服务名称'redis'(Docker环境)
    #         host = os.environ.get('REDIS_HOST', 'redis')
    #         port = int(os.environ.get('REDIS_PORT', 6379))
    #         db = int(os.environ.get('REDIS_DB', 0))
    #         password = os.environ.get('REDIS_PASSWORD', None)
            
    #         print(f"连接到Redis: {host}:{port}")
            
    #         cls._instance = redis.Redis(
    #             host=host,
    #             port=port,
    #             db=db,
    #             password=password,
    #             decode_responses=False  # 不自动解码，因为我们使用pickle进行序列化
    #         )
    #     return cls._instance
    
    #不用docker
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.Redis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=False  # 不自动解码，因为我们使用pickle进行序列化
            )
        return cls._instance

# 序列化和反序列化工具
def serialize_data(data):
    """将数据序列化为二进制格式，支持复杂Python对象"""
    return pickle.dumps(data)

def deserialize_data(data):
    """将二进制数据反序列化为Python对象"""
    if data is None:
        return None
    return pickle.loads(data)

# 延迟执行函数(用于延迟双删)
def delay_task(func, delay=1.0, *args, **kwargs):
    """
    延迟执行任务
    
    参数:
        func: 要执行的函数
        delay: 延迟时间(秒)
        args, kwargs: 传递给func的参数
    """
    def _inner():
        time.sleep(delay)
        func(*args, **kwargs)
    
    # 创建并启动线程
    threading.Thread(target=_inner).start()

# 缓存装饰器
def cache_with_key(key_prefix, ttl=3600):
    """
    Redis缓存装饰器
    
    参数:
        key_prefix: 缓存键前缀
        ttl: 缓存过期时间(秒)，默认1小时
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 构建缓存键 - 避免将对象实例包含在键中
            cache_key = f"{key_prefix}"
            
            # 处理附加参数 - 仅使用非self/cls的参数
            if len(args) > 1:  # 跳过self/cls参数
                args_str = ':'.join(str(arg) for arg in args[1:])
                if args_str:
                    cache_key += f":{args_str}"
            
            # 排序关键字参数以确保相同参数生成相同的键
            if kwargs:
                sorted_kwargs = sorted(kwargs.items())
                kwargs_str = ':'.join(f'{k}={v}' for k, v in sorted_kwargs)
                if kwargs_str:
                    cache_key += f":{kwargs_str}"
            
            # 获取Redis连接
            redis_client = RedisClient.get_instance()
            
            # 尝试从缓存获取数据
            cached_data = redis_client.get(cache_key)
            if cached_data:
                print(f"Cache hit for key: {cache_key}")
                return deserialize_data(cached_data)
            
            # 缓存未命中，执行原函数
            print(f"Cache miss for key: {cache_key}")
            result = func(*args, **kwargs)
            
            # 将结果存入缓存
            redis_client.setex(
                cache_key, 
                ttl,
                serialize_data(result)
            )
            
            return result
        return wrapper
    return decorator

# 删除指定缓存键
def delete_cache_key(cache_key):
    """删除指定的缓存键"""
    redis_client = RedisClient.get_instance()
    redis_client.delete(cache_key)
    print(f"Deleted cache key: {cache_key}")

# 清除指定前缀的缓存
def clear_cache_by_prefix(prefix):
    """
    清除指定前缀的所有缓存
    
    参数:
        prefix: 缓存键前缀
    """
    redis_client = RedisClient.get_instance()
    pattern = f"{prefix}*"
    
    # 使用scan_iter方法查找所有匹配的键
    keys = []
    cursor = 0
    while True:
        cursor, partial_keys = redis_client.scan(cursor, match=pattern, count=100)
        for key in partial_keys:
            keys.append(key)
        if cursor == 0:
            break
            
    # 如果找到匹配的键，则删除它们
    if keys:
        redis_client.delete(*keys)
        print(f"Deleted {len(keys)} cache keys with prefix: {prefix}")
    else:
        print(f"No cache keys found with prefix: {prefix}")
    
    return len(keys)  # 返回删除的键数量

# 延迟双删缓存策略装饰器
def cache_update_with_delay_double_deletion(cache_prefixes, delay=1.0):
    """
    实现延迟双删缓存更新策略的装饰器
    
    步骤:
    1. 先删除相关缓存
    2. 执行数据库操作
    3. 等待一段时间(默认1秒)
    4. 再次删除相关缓存
    
    参数:
        cache_prefixes: 需要清除的缓存前缀列表
        delay: 延迟时间(秒)，默认1秒
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 第一次删除缓存 - 先记录删除了哪些键
            deleted_counts = {}
            for prefix in cache_prefixes:
                count = clear_cache_by_prefix(prefix)
                deleted_counts[prefix] = count
                print(f"First deletion of cache prefix '{prefix}': {count} keys deleted")
            
            # 执行数据库操作
            result = func(*args, **kwargs)
            
            # 延迟执行第二次删除缓存
            for prefix in cache_prefixes:
                # 使用闭包来确保在延迟任务中正确捕获prefix值
                def schedule_deletion(prefix_to_delete=prefix):
                    def delayed_deletion():
                        time.sleep(delay)
                        count = clear_cache_by_prefix(prefix_to_delete)
                        print(f"Second deletion (after {delay}s delay) of cache prefix '{prefix_to_delete}': {count} keys deleted")
                    # 创建并启动线程
                    thread = threading.Thread(target=delayed_deletion)
                    thread.daemon = True  # 设置为守护线程
                    thread.start()
                
                schedule_deletion()
                print(f"Scheduled delayed second deletion of cache prefix: {prefix} in {delay} seconds")
            
            return result
        return wrapper
    return decorator 