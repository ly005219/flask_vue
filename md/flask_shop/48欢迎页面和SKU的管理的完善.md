# welcome页面的完善

## 1：获取上次登录时间后端开发

```python
增加数据库上次登录时间的字段
class User(db.Model, BaseModel):
    __tablename__ = 't_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    pwd = db.Column(db.String(800))
    nick_name = db.Column(db.String(50))
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(50), unique=True)
    last_login = db.Column(db.DateTime)  # 添加最后登录时间字段
     #创建同步数据库对象,$env:FLASK_APP = "manager"
 #传递app和数据库对象,创建完数据库后就进行三步命令：flask db init
 #    flask db migrate -m ''
 #    flask db upgrade

###测试上次登录时间
GET http://127.0.0.1:5000/user/last_login/?username=baizhan
```

```python
登录要刷新时间
#登录功能
@user_bp.route('/login/', methods=[ 'POST'])
def login():

    name=request.get_json().get('username')
    pwd=request.get_json().get('pwd')


    if not all([name, pwd]):

        return {'status':400,'msg':'参数不完整'}
    
    else:
        user=models.User.query.filter(models.User.username==name).first()
        if not user:
            return {'status':400,'msg':'用户不存在'}
        else:
            if user.check_password(pwd):
                            # 更新最后登录时间
                user.last_login = datetime.now()
                db.session.commit()
                #生产token
                token=generate_token({'id':user.id})
                

                return {'status':200,'msg':'登录成功','data':{'token':token}}


              
            else:
                return {'status':400,'msg':'密码错误'}

```



```python
 
@user_bp.route('/last_login/')
def user_last_login():
    # 获取查询参数中的用户名
    username = request.args.get('username')
    if not username:
        return {'status': 400, 'msg': '缺少用户名参数'}
    
    try:
        # 从数据库查询用户
        user = models.User.query.filter_by(username=username).first()
        if not user:
            return {'status': 404, 'msg': '用户不存在'}
            
        # 获取最后登录时间
        last_login = user.last_login
        if last_login:
            # 格式化时间为字符串
            last_login_str = last_login.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_login_str = None
            
        return {
            'status': 200,
            'msg': 'success',
            'data': {
                'last_login': last_login_str
            }
        }
        
    except Exception as e:
        print(f"获取登录时间错误: {str(e)}")
        return {'status': 500, 'msg': '服务器内部错误'}
```

## 2:前端的渲染

```
1.base.js
    get_last_login: "/user/last_login/",  // 获取上次登录时间的接口
 2.index.js
    getLastLogin(username) {
     return axios.get(base.baseUrl + base.get_last_login + `?username=${username}`)
   }
   
```



```vue
<template>
  <div class="welcome-container">
    <!-- 顶部欢迎区域 -->
    <div class="welcome-header">
      <h1>欢迎使用电商后台管理系统</h1>
      <div class="time-info">
        <p>{{ currentTime }}</p>
        <p>{{ greeting }}</p>
      </div>
    </div>

    <!-- 数据概览卡片区域 -->
    <div class="data-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>商品总数</span>
                <el-icon><Goods /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>{{ statistics.products }}</h2>
              <p>较昨日 <span class="up">+10</span></p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>订单数量</span>
                <el-icon><List /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>{{ statistics.orders }}</h2>
              <p>较昨日 <span class="up">+5</span></p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>用户数量</span>
                <el-icon><User /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>{{ statistics.users }}</h2>
              <p>较昨日 <span class="up">+3</span></p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>总收入</span>
                <el-icon><Money /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>¥{{ statistics.income }}</h2>
              <p>较昨日 <span class="up">+1890</span></p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快捷操作区域 -->
    <div class="quick-actions">
      <el-card class="action-card">
        <template #header>
          <div class="card-header">
            <span>快捷操作</span>
          </div>
        </template>
        <div class="action-buttons">
          <el-button type="primary" @click="$router.push('/add_product/')">
            <el-icon><Plus /></el-icon>添加商品
          </el-button>
          <el-button type="success" @click="$router.push('/order_list/')">
            <el-icon><List /></el-icon>查看订单
          </el-button>
          <el-button type="warning" @click="$router.push('/user_list/')">
            <el-icon><User /></el-icon>用户管理
          </el-button>
          <el-button type="info" @click="$router.push('/statistics_list/')">
            <el-icon><DataLine /></el-icon>数据统计
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 系统信息区域 -->
    <div class="system-info">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>系统信息</span>
          </div>
        </template>
        <div class="info-list">
          <p><span>系统版本：</span>{{ systemVersion }}</p>
          <p><span>上次登录：</span>{{ lastLoginTime || '加载中...' }}</p>
          <p><span>浏览器：</span>{{ browserInfo || '加载中...' }}</p>
          <p><span>操作系统：</span>{{ osInfo || '加载中...' }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Goods, List, User, Money, Plus, DataLine } from '@element-plus/icons-vue'
import api from '@/api/index'

// 统计数据
const statistics = ref({
  products: 1234,
  orders: 89,
  users: 456,
  income: '23,678.00'
})

// 时间相关
const currentTime = ref('')
const greeting = ref('')
const lastLoginTime = ref('')

// 系统信息
const browserInfo = ref('')
const osInfo = ref('')
const systemVersion = ref('v1.0.0')

// 更新时间和问候语
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString()
  const hour = now.getHours()
  if (hour < 12) {
    greeting.value = '早上好！开启愉快的一天'
  } else if (hour < 18) {
    greeting.value = '下午好！继续努力'
  } else {
    greeting.value = '晚上好！注意休息'
  }
}

// 获取系统信息
const getSystemInfo = () => {
  // 获取浏览器信息
  const userAgent = navigator.userAgent
  let browser = 'Unknown'
  if (userAgent.indexOf('Chrome') > -1) {
    browser = 'Chrome ' + userAgent.match(/Chrome\/(\d+\.\d+)/)[1]
  } else if (userAgent.indexOf('Firefox') > -1) {
    browser = 'Firefox ' + userAgent.match(/Firefox\/(\d+\.\d+)/)[1]
  } else if (userAgent.indexOf('Safari') > -1) {
    browser = 'Safari ' + userAgent.match(/Safari\/(\d+\.\d+)/)[1]
  }
  browserInfo.value = browser

  // 获取操作系统信息
  let os = 'Unknown'
  if (userAgent.indexOf('Win') > -1) {
    os = 'Windows'
  } else if (userAgent.indexOf('Mac') > -1) {
    os = 'MacOS'
  } else if (userAgent.indexOf('Linux') > -1) {
    os = 'Linux'
  }
  osInfo.value = os
}

// 获取上次登录时间
const getLastLoginTime = () => {
  const username = sessionStorage.getItem('username')
  if (username) {
    api.getLastLogin(username).then(res => {
      if (res.data.status === 200) {
        lastLoginTime.value = res.data.data.last_login || '暂无登录记录'
      }
    }).catch(err => {
      console.error('获取上次登录时间失败:', err)
      lastLoginTime.value = '获取失败'
    })
  }
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
  getSystemInfo()
  getLastLoginTime()
})
</script>

<style scoped>
.welcome-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.welcome-header {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.welcome-header h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #409EFF;
}

.time-info {
  font-size: 16px;
  color: #606266;
}

.data-overview {
  margin-bottom: 30px;
}

.data-card {
  transition: all 0.3s;
}

.data-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  color: #303133;
}

.card-content {
  text-align: center;
}

.card-content h2 {
  font-size: 24px;
  color: #409EFF;
  margin: 10px 0;
}

.up {
  color: #67C23A;
}

.quick-actions {
  margin-bottom: 30px;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 15px;
}

.action-buttons .el-button {
  min-width: 120px;
}

.system-info .info-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-list p {
  margin: 0;
  color: #606266;
}

.info-list p span {
  color: #303133;
  font-weight: bold;
  margin-right: 10px;
}

@media screen and (max-width: 768px) {
  .system-info .info-list {
    grid-template-columns: 1fr;
  }
}
</style>

```



# home.vue的侧边栏固定



```vue
<template>
    <div class="common-layout container">
        <el-container class="container">
            <el-header class="header">
                <div class="logo">
                    <img src="../assets/login1.png" alt="">
                    <span>电商后台管理系统</span>
                </div>

                <div class="user">
                    <el-button @click="logout" type="success" plain>退出登录</el-button>
                </div>
            </el-header>
            
            <el-container class="main-container">
                <el-aside width="200px" class="aside">
                    <el-menu active-text-color="#ffd04b" 
                            background-color="#0d6496" 
                            class="el-menu-vertical-demo"
                            default-active="2" 
                            text-color="#fff" 
                            :unique-opened="true" 
                            router>
                        <el-sub-menu :index="index+' '" v-for="(item, index) in menulist.menus">
                            <template #title>
                                <el-icon>
                                    <component :is="menulist.icons[item.id]"></component>
                                </el-icon>
                                <span>{{ item.name}}</span>
                            </template>
                            <el-menu-item :index="childItem.path" 
                                        v-for="childItem in item.children">
                                {{ childItem.name }}
                            </el-menu-item>
                        </el-sub-menu>
                    </el-menu>
                </el-aside>

                <el-main class="main-content">
                    <router-view/>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'//导入api接口
import { onMounted, reactive} from 'vue'


const menulist = reactive({
    menus: [],
    icons:{
        '1':'User',
        '2':'Tools',
        '3':'Shop',
        '4':'ShoppingCart',
        '5':'PieChart',

    }


})


// 监听页面刷新,DOM渲染完成后执行
onMounted(() => {
    get_menu()

})
const router = useRouter()

const logout = () => {
    //去除token
    sessionStorage.removeItem('token')
    //跳转到登录页面
    router.push('/login/')

}

// const test = () => {
//     api.test_response().then(res => {
//         console.log(res)
//     })

// }
const get_menu = () => {
    //获取菜单数据
    api.get_menu().then(res => {
        // console.log(res)
        menulist.menus = res.data.menus

        })
}



</script>

<style scoped>
/* 容器样式 */
.container {
    height: 100%;
    min-height: 100vh;
}

/* 头部样式 */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    font-size: 20px;
    color: #999;
    height: 50px;
    width: 100%;
}

/* logo样式 */
.logo {
    float: left;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo img {
    width: 80px;
    height: 40px;
    margin-right: 10px;
}

/* 用户区域样式 */
.user {
    float: right;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
}

/* 主容器样式 */
.main-container {
    margin-top: 50px; /* 为固定头部留出空间 */
    height: calc(100vh - 50px); /* 减去头部高度 */
}

/* 侧边栏样式 */
.aside {
    position: fixed;
    left: 0;
    top: 50px; /* 头部高度 */
    bottom: 0;
    width: 200px !important;
    background-color: #0d6496;
    overflow-y: auto; /* 内容过多时显示滚动条 */
    z-index: 999;
}

/* 主内容区域样式 */
.main-content {
    margin-left: 200px; /* 为固定侧边栏留出空间 */
    min-height: calc(100vh - 50px); /* 确保内容区域至少占满剩余高度 */
    background-color: #f0f2f5;
    padding: 20px;
}

/* 滚动条样式优化 */
.aside::-webkit-scrollbar {
    width: 6px;
}

.aside::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
}

.aside::-webkit-scrollbar-track {
    background-color: transparent;
}

/* 菜单样式优化 */
.el-menu {
    border-right: none;
}

/* 确保内容区域不会被覆盖 */
.el-main {
    padding: 20px;
    box-sizing: border-box;
}
</style>

```



## 2：SKU管理

```python
from io import BytesIO
from flask import request, make_response
from openpyxl import Workbook
from flask_shop.sku import sku_api
from flask_restful import Resource, reqparse
from flask_shop import models, db
import time
import random
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment

class SKUs(Resource):
    def get(self):
        """获取SKU列表"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', type=int, location='args')
            args = parser.parse_args()
            
            if args.get('product_id'):
                skus = models.SKU.query.filter_by(product_id=args.get('product_id')).all()
            else:
                skus = models.SKU.query.all()
                
            return {
                'status': 200,
                'msg': '获取SKU列表成功',
                'data': {
                    'total': len(skus),
                    'data': [sku.to_dict() for sku in skus]
                }
            }
        except Exception as e:
            print(f"获取SKU列表错误: {str(e)}")
            return {'status': 500, 'msg': str(e)}

    def post(self):
        """添加SKU"""
        try:
            # 获取请求数据
            name = request.get_json().get('product_id')
            specifications = request.get_json().get('specifications')
            price = request.get_json().get('price')
            stock = request.get_json().get('stock')
            
            # 验证必要字段
            if not all([name, specifications, price, stock]):
                return {'status': 400, 'msg': 'SKU参数不完整'}
            
            # 创建SKU
            sku = models.SKU(
                product_id=name,
                sku_code=self.generate_sku_code(),
                specifications=specifications,
                price=price,
                stock=stock,
                status=1  # 默认上架状态
            )
            
            # 保存到数据库
            db.session.add(sku)
            db.session.commit()
            return {'status': 200, 'msg': '添加SKU成功'}
        except Exception as e:
            db.session.rollback()
            return {'status': 500, 'msg': '添加SKU失败'}

    def generate_sku_code(self):
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        return f"SKU-{timestamp}-{random_num}"

sku_api.add_resource(SKUs, '/skus/')

class SKUManage(Resource):
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float)
        parser.add_argument('stock', type=int)
        parser.add_argument('status', type=int)
        args = parser.parse_args()

        try:
            sku = models.SKU.query.get(id)
            if not sku:
                return {'status': 404, 'msg': 'SKU不存在'}

            if args.get('price'):
                sku.price = args.get('price')
            if args.get('stock') is not None:
                old_stock = sku.stock
                new_stock = args.get('stock')
                sku.stock = new_stock
                
                stock_log = models.StockLog(
                    sku_id=id,
                    change_amount=new_stock - old_stock,
                    type='manual',
                    operator=request.headers.get('username', 'unknown')
                )
                db.session.add(stock_log)
                
            if args.get('status') is not None:
                sku.status = args.get('status')
                
            db.session.commit()
            return {'status': 200, 'msg': '更新SKU成功'}
        except Exception as e:
            db.session.rollback()
            return {'status': 500, 'msg': str(e)}

    def delete(self, id):
        try:
            sku = models.SKU.query.get(id)
            if not sku:
                return {'status': 404, 'msg': 'SKU不存在'}
                
            db.session.delete(sku)
            db.session.commit()
            return {'status': 200, 'msg': '删除SKU成功'}
        except Exception as e:
            db.session.rollback()
            return {'status': 500, 'msg': '删除SKU失败'}

sku_api.add_resource(SKUManage, '/sku/<int:id>/')

class SKUExport(Resource):
    def get(self):
        """导出SKU列表为Excel"""
        try:
            # 获取所有SKU数据
            skus = models.SKU.query.all()
            
            # 创建工作簿
            wb = Workbook()
            ws = wb.active
            ws.title = "SKU列表"
            
            # 设置列宽
            column_widths = {
                'A': 15,  # SKU编码
                'B': 10,  # 商品ID
                'C': 30,  # 规格
                'D': 12,  # 价格
                'E': 10,  # 库存
                'F': 10,  # 销量
                'G': 10,  # 状态
            }
            
            for col, width in column_widths.items():
                ws.column_dimensions[col].width = width
            
            # 定义样式
            header_fill = PatternFill(start_color='1E90FF', end_color='1E90FF', fill_type='solid')
            header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
            data_font = Font(name='微软雅黑', size=10)
            
            # 边框样式
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            # 对齐方式
            center_aligned = Alignment(horizontal='center', vertical='center', wrap_text=True)
            left_aligned = Alignment(horizontal='left', vertical='center', wrap_text=True)
            
            # 写入表头
            headers = ['SKU编码', '商品ID', '规格', '价格', '库存', '销量', '状态']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_aligned
                cell.border = thin_border
            
            # 写入数据
            for row, sku in enumerate(skus, 2):
                # 格式化规格信息
                specs_str = '\n'.join([f"{k}: {v}" for k, v in sku.specifications.items()])
                
                row_data = [
                    sku.sku_code,
                    sku.product_id,
                    specs_str,
                    f"¥{sku.price:.2f}",
                    sku.stock,
                    sku.sales,
                    '上架' if sku.status == 1 else '下架'
                ]
                
                # 设置每个单元格的样式
                for col, value in enumerate(row_data, 1):
                    cell = ws.cell(row=row, column=col, value=value)
                    cell.font = data_font
                    cell.border = thin_border
                    
                    # 规格列左对齐，其他居中
                    if col == 3:  # 规格列
                        cell.alignment = left_aligned
                    else:
                        cell.alignment = center_aligned
                    
                    # 设置交替行颜色
                    if row % 2 == 0:
                        cell.fill = PatternFill(start_color='F5F5F5', end_color='F5F5F5', fill_type='solid')
            
            # 保存到内存
            excel_file = BytesIO()
            wb.save(excel_file)
            excel_file.seek(0)
            
            # 准备响应
            response = make_response(excel_file.getvalue())
            response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response.headers['Content-Disposition'] = 'attachment; filename=sku_list.xlsx'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,token'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            
            return response
            
        except Exception as e:
            print(f"Excel导出错误: {str(e)}")
            return {'status': 500, 'msg': '导出失败'}

sku_api.add_resource(SKUExport, '/skus/export/excel/') 
```



```vue
<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>SKU管理</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
      <div class="button-group">
        <el-button type="primary" @click="showAddDialog">添加SKU</el-button>
        <el-button type="success" @click="exportExcel">导出Excel</el-button>
      </div>
      
      <el-table :data="skuList" style="width: 100%; margin-top: 20px">
        <el-table-column prop="sku_code" label="SKU编码" />
        <el-table-column prop="specifications" label="规格">
          <template #default="scope">
            <div v-for="(value, key) in scope.row.specifications" :key="key">
              {{ key }}: {{ value }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" />
        <el-table-column prop="stock" label="库存" />
        <el-table-column prop="sales" label="销量" />
        <el-table-column label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="scope">
            <el-button-group>
              <el-button 
                type="primary" 
                @click="editSKU(scope.row)"
                :icon="Edit"
              >编辑</el-button>
              <el-button 
                type="danger" 
                @click="deleteSKU(scope.row)"
                :icon="Delete"
              >删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑SKU对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="50%">
      <el-form :model="skuForm" ref="skuFormRef" :rules="skuRules" label-width="80px">
        <el-form-item label="商品" prop="product_id">
          <el-select v-model="skuForm.product_id" placeholder="请选择商品">
            <el-option
              v-for="item in productList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="规格" prop="specifications">
          <div v-for="(spec, index) in specifications" :key="index" class="spec-item">
            <el-input v-model="spec.name" placeholder="规格名称" style="width: 200px" />
            <el-input v-model="spec.value" placeholder="规格值" style="width: 200px; margin-left: 10px" />
            <el-button @click="removeSpec(index)" type="danger" icon="Delete" circle class="spec-delete" />
          </div>
          <el-button @click="addSpec" type="primary" style="margin-top: 10px">添加规格</el-button>
        </el-form-item>

        <el-form-item label="价格" prop="price">
          <el-input v-model.number="skuForm.price" type="number" placeholder="请输入价格" />
        </el-form-item>

        <el-form-item label="库存" prop="stock">
          <el-input v-model.number="skuForm.stock" type="number" placeholder="请输入库存" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitSKU">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import { Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api/index'
import base from '@/api/base'

const skuList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加SKU')
const productList = ref([])
const specifications = ref([])

const skuForm = reactive({
  product_id: '',
  price: '',
  stock: '',
  specifications: {}
})

const skuRules = {
  product_id: [{ required: true, message: '请选择商品', trigger: 'change' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }]
}

onMounted(() => {
  getSKUList()
  getProductList()
})

const getSKUList = () => {
  api.get_sku_list()
    .then(res => {
      console.log('SKU列表响应:', res)
      if (res?.data?.status === 200) {
        skuList.value = res.data.data.data || []
      } else {
        ElMessage.error(res?.data?.msg || '获取SKU列表失败')
      }
    })
    .catch(err => {
      console.error('获取SKU列表错误:', err)
      ElMessage.error('获取SKU列表失败，请检查网络连接')
    })
}

const getProductList = () => {
  api.get_product_list().then(res => {
    if (res.data && res.data.status === 200) {
      productList.value = res.data.data.data || []
    } else {
      ElMessage.error(res.data?.msg || '获取商品列表失败')
    }
  }).catch(err => {
    console.error('获取商品列表错误:', err)
    ElMessage.error('获取商品列表失败')
  })
}

const showAddDialog = () => {
  dialogTitle.value = '添加SKU'
  dialogVisible.value = true
  specifications.value = []
}

const addSpec = () => {
  specifications.value.push({
    name: '',
    value: ''
  })
}

const removeSpec = (index) => {
  specifications.value.splice(index, 1)
}

const submitSKU = () => {
  // 数据验证
  if (!skuForm.product_id) {
    ElMessage.error('请选择商品')
    return
  }
  if (!skuForm.price || skuForm.price <= 0) {
    ElMessage.error('请输入有效的价格')
    return
  }
  if (!skuForm.stock || skuForm.stock < 0) {
    ElMessage.error('请输入有效的库存')
    return
  }
  if (specifications.value.length === 0) {
    ElMessage.error('请至少添加一个规格')
    return
  }

  // 将规格数组转换为对象
  const specs = {}
  for (const spec of specifications.value) {
    if (!spec.name || !spec.value) {
      ElMessage.error('规格名称和值不能为空')
      return
    }
    specs[spec.name] = spec.value
  }

  // 准备提交的数据
  const submitData = {
    product_id: parseInt(skuForm.product_id),
    specifications: specs,
    price: parseFloat(skuForm.price),
    stock: parseInt(skuForm.stock)
  }

  if (dialogTitle.value === '添加SKU') {
    api.add_sku(submitData)
      .then(res => {
        if (res.data.status === 200) {
          ElMessage({
            showClose: true,
            message: res.data.msg,
            type: 'success'
          })
          dialogVisible.value = false
          getSKUList()
          // 重置表单
          skuForm.product_id = ''
          skuForm.price = ''
          skuForm.stock = ''
          specifications.value = []
        } else {
          ElMessage.warning({
            showClose: true,
            message: res.data.msg
          })
        }
      })
      .catch(err => {
        console.error('添加SKU错误:', err)
        ElMessage.warning({
          showClose: true,
          message: '添加SKU失败，请检查网络连接'
        })
      })
  } else {
    api.update_sku(skuForm.id, skuForm).then(res => {
      if (res.data.status === 200) {
        ElMessage({
          showClose: true,
          message: res.data.msg,
          type: 'success'
        })
        dialogVisible.value = false
        getSKUList()
      } else {
        ElMessage.warning({
          showClose: true,
          message: res.data.msg
        })
      }
    })
  }
}

const editSKU = (row) => {
  dialogTitle.value = '编辑SKU'
  dialogVisible.value = true
  Object.assign(skuForm, row)
  
  // 将规格对象转换为数组
  specifications.value = []
  for (let key in row.specifications) {
    specifications.value.push({
      name: key,
      value: row.specifications[key]
    })
  }
}

const deleteSKU = (row) => {
  ElMessageBox.confirm(`确认删除${row.sku_code}商品吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    api.delete_sku(row.id).then(res => {
      if (res.data.status === 200) {
        ElMessage({
          showClose: true,
          message: res.data.msg,
          type: 'success'
        })
        getSKUList()
      } else {
        ElMessage.warning({
          showClose: true,
          message: res.data.msg
        })
      }
    })
  }).catch(() => {
    ElMessage({
      type: 'info',
      message: '已取消删除'
    })
  })
}

const exportExcel = () => {
  fetch(base.baseUrl + base.export_sku_excel, {
    method: 'GET',
    headers: {
      'token': sessionStorage.getItem('token')
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    return response.blob()
  })
  .then(blob => {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'sku_list.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('Excel导出成功')
  })
  .catch(err => {
    console.error('导出Excel失败:', err)
    ElMessage.error('导出Excel失败')
  })
}
</script>

<style scoped>
.box-card {
  margin-top: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.el-button-group {
  display: flex;
  gap: 5px;
}

.el-button-group .el-button {
  padding: 8px 16px;
  font-size: 14px;
}

.spec-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.spec-delete {
  margin-left: 10px;
}

/* 确保操作按钮列的宽度足够 */
:deep(.el-table .cell) {
  white-space: nowrap;
}

/* 调整图标和文字的间距 */
:deep(.el-button [class*='el-icon'] + span) {
  margin-left: 6px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style> 
```

