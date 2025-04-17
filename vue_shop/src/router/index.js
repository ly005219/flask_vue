import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [

  {
    path: '/login/',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    redirect: '/welcome/',
    children: [

      {
        path:'/welcome/',
        name: 'welcome',
        component: () => import('../views/WelcomeView.vue')


      },

      {
        path:'/user_list/'
        ,name: 'user_list',
        component: () => import('../views/UserView.vue')
      },
      {
        path:'/permission_list/'
        ,name: 'permission_list',
        component: () => import('../views/MenuView.vue')

      },
      {
        path:'//role_list/',
        name: 'role_list',
        component: () => import('../views/RoleView.vue')


      },

      {
        path:'/category_list/'
        ,name: 'category_list',
        component: () => import('../views/CategoryView.vue')
      },

      {
        path:'/attribute_list/',
        name: 'attribute_list',
        component: () => import('../views/AttributeView.vue')
      },
      {
        path:'/product_list/',
        name: 'product_list',
        component: () => import('../views/ProductView.vue')

      },
      {
        path:'/add_product/'
        ,name: 'add_product',
        component: () => import('../views/AddProductView.vue')

      },
      {
        path:'/order_list/',
        name: 'order_list',
        component: () => import('../views/OrderView.vue')

      },
      {
        path:'/statistics_list/'
        ,name:'statistics_list',
        component: () => import('../views/StatisticsView.vue')
      },
      {
        path: '/sku_manage/',
        name: 'SKUManage',
        component: () => import('../views/SKUView.vue'),
        meta: { title: 'SKU管理' }
      },
      {
        path: '/my_permissions/',
        name: 'UserPermissions',
        component: () => import('../views/UserPermissions.vue'),
        meta: { title: '我的权限' }
      }

      


    ]
  },
 
  



]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router


//做router跳转的login_required的验证
router.beforeEach((to, from, next) => {
  if (to.path === '/login/') {
    next()

  }else{
    //获取token值
    const token = sessionStorage.getItem('token') 
    if (!token ){
      next('/login/')
    }
    next()


  }


})



