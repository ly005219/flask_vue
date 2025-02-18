## 1：注册时只能用唯一的邮箱和电话

```python
 class UserReigster(Resource):
    def post(self):
        username=request.get_json().get('username')
        pwd=request.get_json().get('pwd')
        email=request.get_json().get('email')
        nick_name=request.get_json().get('nick_name')
        phone=request.get_json().get('phone')
        real_pwd=request.get_json().get('real_pwd')
        if not all([username,pwd,real_pwd]):
             return {'status':400,'msg':'参数不完整'}
        else:
            if len(pwd)<6 or len(pwd)>20:
                return {'status':400,'msg':'密码长度不能小于6,也不能大于20'}
            if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
                return {'status':400,'msg':'邮箱格式不正确'}
            if not re.match(r'^1[3-9]\d{9}$',phone):
                return {'status':400,'msg':'手机号格式不正确'}
        #接收角色id信息
        role_id=request.get_json().get('role_id')

        



        try:
            user=models.User.query.filter(models.User.username==username).first()
            if user:
                return {'status':400,'msg':'用户名已存在'}
              # 验证邮箱是否存在
            check_email_response = check_email()
            if check_email_response['status'] == 400:
                return check_email_response
            # 验证手机号是否存在
            check_phone_response = check_phone()
            if check_phone_response['status'] == 400:
                return check_phone_response
        except Exception as e:
            return f'status:500------->msg:{e}'
         
        if real_pwd==pwd:
            if not role_id:
                new_user=models.User(username=username,password=pwd,email=email,nick_name=nick_name,phone=phone)
            else:
                new_user=models.User(username=username,password=pwd,email=email,nick_name=nick_name,phone=phone,role_id=role_id)
                
            
            db.session.add(new_user)
            db.session.commit()
            return {'status':200,'msg':'注册成功'}
        else:
            return {'status':400,'msg':'两次密码不一致'}




#验证邮箱是否存在
@user_bp.route('/check_email/',methods=['POST'])
def check_email():

    email=request.get_json().get('email')
    check_email=models.User.query.filter(models.User.email==email).first()
    if check_email:
        return {'status':400,'msg':'邮箱已存在'}
    else:
        return {'status':200,'msg':'邮箱可用'}


#验证手机号是否存在
@user_bp.route('/check_phone/',methods=['POST'])
def check_phone():

    phone=request.get_json().get('phone')
    check_phone=models.User.query.filter(models.User.phone==phone).first()
    if check_phone:
        return {'status':400,'msg':'手机号已存在'}
    else:
        return {'status':200,'msg':'手机号可用'}
```



```vue
<template #footer>
            <div class="dialog-footer">
                <el-button @click="addFormRest">取消</el-button>
                <el-button type="primary" @click="addUser(addFormRef)">
                    确认
                </el-button>
            </div>
        </template>

<script>
//增加用户弹窗相关数据,注册
const addUser = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('验证成功')
            api.register_user(user_form).then(res => {
                //根据响应的状态码进行不同的操作
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //重置表单
                    addFormRest()
                    //刷新页面，添加数据后自动刷新不用点击搜索之后在触发这个刷新的get_user_list()函数
                    get_user_list()
              

                }else{
                    //如果res.data.status ! == 200，说明验证失败，弹出错误信息res.data.msg
                    ElMessage.error({
                        showClose: true,
                        message: res.data.msg});
                   
                    
                    
                    console.log(res.data.msg)
                }
             
            })

        } else {
            console.log('验证失败')
            
          
            return false
        }


    })

}
</script>
```



## 2:删除用户时，由于下面的t_orders订单表的user_id字段关联了user的id字段，所以得设置user_id为级联删除，才能删除成功，否则只能先删除订单表里面的所有与该用户相关联的订单。



