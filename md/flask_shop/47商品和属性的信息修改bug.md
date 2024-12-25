## 1:商品的信息修改



```py
    def put(self, id):
        '''
        修改商品
        '''
        #获取参数
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('number', type=int)
        parser.add_argument('state', type=int)

        args = parser.parse_args()
        #根据id查询商品
        try:
            product = models.Product.query.get(id)
            #修改商品信息
            if args.get('name'):
                product.name = args.get('name')
            if args.get('price'):
                product.price = args.get('price')
            if args.get('number'):
                product.number = args.get('number')
            if args.get('state'):
                product.state = args.get('state')
            #提交数据
            models.db.session.commit()
            #返回结果
            return {'status': 200, 'msg': '修改商品成功'}
        except Exception as e:
            print(e)
            return {'status': 500, 'msg': '修改商品失败'}
      '''
PUT http://127.0.0.1:5000/product/23/
Content-Type: application/json

{
    "name": "超级火龙果",
    "price": 199,
    "number": 100,
    "state": 2
}
'''
```



```vue

        <!-- 编辑商品弹框 -->
         <el-dialog title="编辑商品" v-model="ProductEditDialogVisible" width="30%" :before-close="handleClose">
            <el-form  :model="productEditForm" >
                <el-form-item label="商品名称" prop="name">
                    <el-input v-model="productEditForm.name" clearable></el-input>
                </el-form-item>
                <el-form-item label="商品价格" prop="price">
                    <el-input v-model="productEditForm.price" clearable></el-input>
                </el-form-item>
                <el-form-item label="商品数量" prop="number">
                    <el-input v-model="productEditForm.number" clearable></el-input>
                </el-form-item>
                <el-form-item label="商品状态" prop="state">
                    <el-select v-model="productEditForm.state" placeholder="请选择商品状态">
                        <!-- value绑定在表单的state字段上,label是显示的选项 -->
                        <el-option label="上架" value="1"></el-option>
                        <el-option label="下架" value="0"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="ProductEditDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="ProductEditSubmit">确 定</el-button>
            </div>
        </el-dialog>

<script>
//编辑商品弹框
const ProductEditDialogVisible = ref(false)
const productEditForm = reactive({
    name: '',
    price: '',
    number: '',
    state: ''
})

const tmpdata = reactive({
    name: '',
    price: '',
    number: '',
    state: ''
    })

const productEditID = ref('')
const ProductEdit = (index, row) => {
    productEditForm.name = row.name
    productEditForm.price = row.price
    productEditForm.number = row.number
    productEditForm.state = row.state 


    ProductEditDialogVisible.value = true
    productEditID.value= row.id


    // 保存原始产品数据的变量
    tmpdata.name = row.name
    tmpdata.price = row.price
    tmpdata.number = row.number
    tmpdata.state = row.state

}
// 保存原始产品数据的变量

const ProductEditSubmit = () => {
    // 输出表单内容
    console.log(productEditForm)
    
    // 直接调用 API 接口进行更新
    api.update_product(productEditID.value, productEditForm).then(res => {
        if (res.data.status == 200) {
            // 弹出提示框
            ElMessage({
                showClose: true,
                message: res.data.msg,
                type: 'success',
            });

            console.log(res);
            // 刷新查询显示商品数据页面
            getProductList();

            // 关闭编辑对话框
            ProductEditDialogVisible.value = false;
        } else {
            // 如果返回的状态不是200，弹出警告信息
            ElMessage.warning({
                showClose: true,
                message: res.data.msg
            });
        }
    }).catch(error => {
        // 处理请求错误
        console.error(error);
        ElMessage.error({
            showClose: true,
            message: '更新失败，请填写所有信息并重试。'
        });
        productEditForm.name=tmpdata.name
        productEditForm.price=tmpdata.price
        productEditForm.number=tmpdata.number
        productEditForm.state=tmpdata.state


    });
}


const ProductEditCancel = () => {
    ProductEditDialogVisible.value = false
    //清空表单
    productEditForm.name = ''
    productEditForm.price = ''
    productEditForm.number = ''
    productEditForm.state = ''
    }


const handleClose = () => {
    addDialogVisible.value = false
   
    //清空表单
    productEditForm.name = ''
    productEditForm.price = ''
    productEditForm.number = ''
    productEditForm.state = ''
}


```



## 2:属性的更新

### 2.1:动态属性更新

```vue


     <!-- 编辑动态属性弹窗 -->
     <el-dialog v-model="editDialogVisible" title="编辑动态属性" width="30%" >
                <el-form :model="editForm" >
                    <el-form-item label="属性名称" prop="name">
                        <el-input v-model="editForm.name" placeholder="请输入属性名称"></el-input>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="editAttr">
                        确定
                    </el-button>
                    <el-button @click="editDialogVisible = false">取消</el-button>
                </div>


            
            </el-dialog>
<script>
const editDialogVisible = ref(false)
const editForm = reactive({
    name: '',
    id: '',
})

const editClick = (index,row) => {
    editForm.name = row.name
    editForm.id = row.id
    editDialogVisible.value = true
}

const editAttr = () => {
    let params = {
        "name": editForm.name,
        }
    api.update_attr(editForm.id,params).then(res => {
        if (res.data.status == 200) {
            //弹出框
            ElMessage({
                showClose: true,
                message: res.data.msg,
                type: 'success',
            })

            //刷新查询显示商品数据页面
            get_attr_by_category(options.selectID[2],activeName.value)
            editDialogVisible.value = false
        } else {
            ElMessage.warning({
                showClose: true,
                message: res.data.msg});
                // console.log(res.data.msg)
            }
    })



}
```



### 2.2:静态属性的更新



```python
class static_attr(Resource):
    def put(self,id):
        try:
            #创建一个RequestParser对象，用于解析请求参数
            parser = reqparse.RequestParser()
            #添加参数规则
            parser.add_argument('name', type=str)
            parser.add_argument('value', type=str)
            #解析参数
            args = parser.parse_args()
            #获取参数
            attribute = models.Attribute.query.get(id)
            if args.get('name'):
                attribute.name = args.get('name')
            if args.get('value'):
                attribute.value = args.get('value')
            #保存到数据库
            db.session.commit()
            return {'status':200 ,'msg':'修改属性成功success'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'修改属性失败error'}
        
attribute_api.add_resource(static_attr, '/static_attr/<int:id>/')
```

```vue

        <!-- 编辑静态属性弹窗 -->
         <el-dialog v-model="editStaticDialogVisible" title="编辑静态属性" width="30%">
            <el-form :model="editStaticForm" >
                <el-form-item label="属性名称" prop="name">
                    <el-input v-model="editStaticForm.name" placeholder="请输入属性名称"></el-input>
                </el-form-item>
                <el-form-item label="属性值" prop="value">
                    <el-input v-model="editStaticForm.value" placeholder="请输入属性值"></el-input>
              
                </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="editStaticAttr">
                    确定
                </el-button>
                <el-button @click="editStaticDialogVisible = false">取消</el-button>
            </div>



        </el-dialog>


<script>
const editStaticDialogVisible = ref(false)
const editStaticForm = reactive({
    name: '',
    value: '',
    id: '',
})

const editStaticClick = (index,row) => {
    editStaticForm.name = row.name
    editStaticForm.value = row.value
    editStaticForm.id = row.id
    editStaticDialogVisible.value = true
}

const editStaticAttr = () => {
    let params = {
        "name": editStaticForm.name,
        "value": editStaticForm.value,
        }
    api.update_static_attr(editStaticForm.id,params).then(res => {
        if (res.data.status == 200) {
            //弹出框
            ElMessage({
                showClose: true,
                message: res.data.msg,
                type: 'success',
            })

            //刷新查询显示商品数据页面
            get_attr_by_category(options.selectID[2],activeName.value)
            editStaticDialogVisible.value = false
        } else {
            ElMessage.warning({
                showClose: true,
                message: res.data.msg});
                // console.log(res.data.msg)
            }
    })



}
```



## 3：属性的删除

在删除 `t_attributes` 表中的一行，但这行被 `t_product_attrs` 表中的外键引用。换成级联

```javascript
const deleteAttr = (index,row) => {
    console.log(index)
    
    ElMessageBox.confirm('确认删除'+row.name+'商品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
            api.del_attr(row.id).then(res => {
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //刷新查询显示商品数据页面
                    get_attr_by_category(options.selectID[2],activeName.value)

                    } else {
                        ElMessage.warning({
                            showClose: true,
                            message: res.data.msg});
                        // console.log(res.data.msg)
                    }
            })
        }).catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除'
            })
        })
    }
/*DELETE http://127.0.0.1:5000/attribute/43/

    #根据属性id删除属性信息
    def delete(self,id):
        try:
            #根据id获取属性信息
            attribute = models.Attribute.query.get(id)
            #删除属性信息
            db.session.delete(attribute)
            db.session.commit()
            return {'status':200 ,'msg':'删除属性成功'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'删除属性失败'}
        

```

