import time
import functools
def timer(threshold):#接受一个参数阈值
	#因为他是装饰器生成器，肯定也会有个装饰器
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kwagrs):
			start_time=time.time()
			result=func(*args,**kwagrs)
			end_time=time.time()
			if end_time-start_time>threshold:
				print(f'{func.__name__} 运行超时')
			
			return result
		return wrapper
	return decorator
	
#设置一个会睡0.4s的函数，用timer把他的阈值设置为0.2,执行成功说明他确实被装饰了
@timer(0.2)#等价于sleep_04=timer(0.2)(sleep_04),前面的timer(0.2)是装饰器后面是函数闯进去，达到装饰的目的
def sleep_04():
	time.sleep(0.4)
sleep_04()
sleep_04=timer(0.2)(sleep_04)
 #现在说一下装饰后函数的属性
print(sleep_04.__name__)#输出wrapper
#这也可以理解，因为装饰器生成器返回的wrapper函数，所以他的名字就是wrapper，但是我们希望wrapper可以继承func的属性，所以我们可以在wrapper上面加一行
#import functools
#@functools.wraps(func)
#这样就能继承func的属性了
