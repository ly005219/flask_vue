from functools import wraps
from flask import current_app,request
import jwt
import time

'''
    1:加密的数据
        user_id
    2:加密算法
        pip install pwjwt

    3:加密的秘钥
    config.py里面有SECRET_KEY

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
        data = jwt.decode(data, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except Exception as e:
        print(f"Token verification error: {e}")  # 打印错误信息
        return None
    return data


def login_required(view_func):
    @wraps(view_func)
    def verify_token_info(*agrs,**kwagrs):
        token=request.headers.get('token')
        if verify_token(token):#如果这个token为真(不为空并且为原来用户登录的token)
             return view_func(*agrs,**kwagrs)
        else:
            return {'status': 401, 'msg': 'token过期或者无效'}
    return verify_token_info
    