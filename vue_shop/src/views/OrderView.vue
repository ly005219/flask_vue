<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>订单管理</el-breadcrumb-item>
        <el-breadcrumb-item>订单列表</el-breadcrumb-item>

    </el-breadcrumb>

    <el-card class="box-card">
        <!-- 一个搜索按钮 -->
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input v-model="order_data.queryName" placeholder="请输入要搜索的订单用户" @input="handleInput" clearable
                    @clear="getOrderList" @keyup.enter="getOrderList">
                    <template #append>
                        <el-button :icon="Search" @click="getOrderList" />
                    </template>
                </el-input>
            </el-col>

        </el-row>

        <el-row>
            <el-table :data="order_data.orderList" style="width: 100%;margin-top: 15px;" stripe>
                <!-- 从数据库获取的数据首先会赋值到productList中，然后在el-table中显示,所以这里的prop要和数据库中字段名一致 -->
                <!-- 也就是prop绑定在:data中对应的数据字段,data里面的数据由数据库返回 -->
                <el-table-column type="index" width="50" />
                <el-table-column label="订单用户" prop="user" width="150"></el-table-column>

                <el-table-column label="订单价格" prop="price" width="150"></el-table-column>
                <el-table-column label="订单数量" prop="number" width="150"></el-table-column>
                <el-table-column label="是否发货" prop="deliver_status" width="150">
                    <template #default="scope">
                        <el-tag type="success" v-if="scope.row.deliver_status === 1">已发货</el-tag>
                        <el-tag type="danger" v-else>未发货</el-tag>

                    </template>


                </el-table-column>
                <el-table-column label="是否支付" prop="pay_status" width="150">
                    <template #default="scope">
                        <el-tag type="success" v-if="scope.row.pay_status === 1">已支付</el-tag>
                        <el-tag type="danger" v-else>未支付</el-tag>



                    </template>
                </el-table-column>

                <el-table-column label="操作">
                    <template #default="scope">

                        <el-button type="primary" :icon="Promotion" @click="showExpress(scope.row.id)">查看物流</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>

        <!-- <el-dialog v-model="expressDialogVisible" title="查看物流">
            <el-timeline style="max-width: 600px">
                <el-timeline-item v-for="(activity, index) in express_info.data" :key="index" :timestamp="activity.update_time">
                    {{ activity.content }}
                </el-timeline-item>
            </el-timeline>



        </el-dialog> -->
        <el-dialog v-model="expressDialogVisible" title="查看物流">
            <el-timeline style="max-width: 600px">
                <el-timeline-item v-for="(activity, index) in express_info.data" :key="index"
                    :timestamp="activity.update_time" :color="index === 0 ? '#ff69b4' : '#90ee90'"
                    :icon="index !== 0 ?  Select: Position"
                    >
                    {{ activity.content }}
                </el-timeline-item>
            </el-timeline>
        </el-dialog>

       




    </el-card>



</template>

<script setup>
//面包屑的图标,搜索按钮的图标
import { ArrowRight, Promotion, Search, Position, Select } from '@element-plus/icons-vue'
import { ref, reactive, onMounted } from 'vue'
import api from '@/api/index'

const order_data = reactive({
    queryName: '',
    orderList: [],

})
let expressDialogVisible = ref(false)
//定义物流信息
let express_info = reactive({
    data: []
})


onMounted(() => {
    getOrderList()
})

const getOrderList = () => {
    let params = {
        'name': order_data.queryName,//这个name是数据库中字段名,会直接携带这个name到接口里面
    }

    api.get_order_list({ params }).then(res => {

        console.log(res.data.orders)
        //打印这个name
        console.log(order_data.queryName)
        order_data.orderList = res.data.orders

    })
}

const handleInput = () => {
    if (order_data.queryName !== '') {
        getOrderList()
    } else {
        getOrderList()
    }

    //lastQueryName.value = product_data.queryName

}
let order_id = ''
const showExpress = (id) => {
    expressDialogVisible.value = true
    order_id = id//这个id就是订单id
    api.get_express_list(order_id).then(res => {
        console.log(res.data)
        express_info.data = res.data.expresses
        console.log(express_info.data)
    })

}

</script>


<style scoped>
.box-card {
    margin-top: 20px;
}
</style>
