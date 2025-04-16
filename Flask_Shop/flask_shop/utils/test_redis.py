# 创建测试脚本验证Redis连接
import redis

# 使用与应用相同的连接参数
r = redis.Redis(host='localhost', port=6379, db=0)

# 设置测试键
r.set('test_key', 'test_value')

# 验证是否可以获取
print(f"Test key exists: {r.exists('test_key')}")
print(f"Value: {r.get('test_key')}")

# 列出所有键
print("All keys:")
for key in r.keys('*'):
    print(f"- {key}")
