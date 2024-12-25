## 1：编写token代码

### 1：因为token也是一个工具类，就在flask_shop项目目录下建一个utlils文件夹，然后建token.py文件,用装饰器检查token是否有用

```python
from flask import current_app,flask
import jwt


    '''
    1:加密的数据
        user_id
    2:加密算法
        pip install pwjwt

    3:加密的秘钥
    config,py里面有SECRET_KEY

    '''
def generate_token(data):
    #设置token的过期时间,JWT_EXPIRATION_DELTA是配置文件里面的一个参数设置好了时间
    data.update({'exp':time.time()+current_app.config['JWT_EXPIRATION_DELTA']})
    #后面的algorithm是加密算法
    token=jwt.encode(data,current_app.config['SECRET_KEY'],algorithm='HS256')
    return token

#数据的解密
def verify_token(data):
    try:
        data=jwt.decode(data,current_app['SECRET_KEY'],algorithms=['HS256'])
    except Exception as e:
        return None
    return data
    
def login_required(view_func):
    @wraps(view_func)
    def verify_token_info(*agrs,**kwagrs):
        token=request.headers.get('token')
        if verify_token(token):#如果这个token为真(不为空并且为原来用户登录的token)
             return view_func(*args, **kwargs)
        else:
            return {'code': 400, 'msg': 'token过期或者无效'}
    return verify_token_info
    

```

## 2:views.py中登录成功后生成token,

```python
import request
from flask_shop.user import user_bp
from flask_shop import models


@user_bp.route('/login/',methods=['POST'])
def login():
    name=request.get_json.get('username')
	pwd=request.get_json.get('pwd')
    
    if not all([name,pwd]):
        return {'status':400,'msg':'参数不完整'}
    else:
        user=models.User.query(name==models.User.username).first()
        if user and user.check_password(pwd):
            #生成token
            token=generate_token(user.id)
            return {'status':200,'msg':'登录成功','data':{'token':token}}
        else:
            return {'status':400,'msg':'用户名或密码错误'}

    
        

        
```



```python
#装饰器介绍：接受一个函数作为参数，根据这个传入的函数定义一个新的函数，新函数传入函数功能的同时，扩充其他的功能，装饰器将新函数返回，在代码里面我们可以使用新传入的函数代替原来传入的函数，

def decorator(func)；#定义一个装饰器decorator，接受一个参数func
	1#定义一个新函数，然后最后返回这个函数,wrapper作为要代替func的新函数，那么他的参数也要和func一样，当我们不知道func参数传进来的是什么，所以我们传*agrs,**kwagrs
	def wrapper(*agrs,**kwagrs):
		3#这里可以来扩充其他功能，这里我加个字符串
		print(f'{func.__name__} is running')
	2#wrapper应该可以运行本来func的功能，所以我使用result来存储本来的func,也要将他返回
		result=func(*agrs,**kwagrs)
		return result
	return wrapper
	
然后这就是一个最简单的装饰器的例子，下面我写一个计算时间的装饰器
def square(x):
	return x*x

import time
def decorator(func)：
	def wrapper(*agrs,**kwagrs):
		start_time=time.time()
		result=fun(*args,**kwargs)
		end_time=time.time()
		print(f'{func.__name__} 运行时间：{end_time-start_time}'
		return result
		
	return wrapper

#使用方法，直接用要使用的函数传给装饰器
decorated_square=decorator(square)#这个decorated_square就是一个函数,wrapper,下面在传递square函数的参数
decorated_square(10)

#还提供了一直更方便的方式,所以@decorator等价于decorator(square)，下次就直接用函数名调用
@decorator
def square(x):
	return x*x

square(10)

#现在我不仅想要实现这个函数能够测量时间，我还要知道这个函数的运行时间时候超过了阈值，我们可以定义一个定义装饰器的函数，暂时把他叫做装饰器生成器
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
   
              
```



## 3:在view测试装饰器

```python
@user_bp.route('/test_login/', methods=['POST'])
@ogin_required
def test_login():
    return {'status':200,'msg':'token验证成功'}

```





## 4：在user.http中测试即可

按照先注册在登录在测试的顺序来，这个token是根据 token=jwt.encode(*data*, current_app.config['SECRET_KEY'], *algorithm*='HS256')data为id（ token=generate_token({'id':user.id})#传递的必须是字典），和时间戳，算法，密钥来生成的所以每次都不一样。

```http
POST  http://127.0.0.1:5000/user/login/
Content-Type: Application/json

{
    "username": "ly",
    "pwd": "123456789"
}

###测试用户注册
###前面的参数名，是name=request.get_json().get('username')里面的get值
POST  http://127.0.0.1:5000/user/register/
Content-Type: Application/json

{
    "username": "ly",
    "pwd": "123456789",
    "real_pwd": "123456789",
    "email": "123456788@qq.com",
    "phone": "12345678902",
    "nick_name":"小样"
   
}

###测试登录装饰器是否有用
GET  http://127.0.0.1:5000/user/test/
token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiZXhwIjoxNzI5ODgwNjI1Ljk0MDExNjR9.2_p6nYJU12jJQ1jiUIdvIL97b5uSLwF7X921jrLVPSI

```

















