<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>添加商品</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
        <el-alert title="下面输入要《添加商品》的信息" type="warning" center />
        <el-steps :active="active" finish-status="success" align-center>
            <el-step title="基本信息" />
            <el-step title="商品静态属性" />
            <el-step title="商品动态属性" />
            <el-step title="商品图片" />
            <el-step title="商品内容" />
            <el-step title="完成" />

        </el-steps>


        <!-- before-leave	切换标签之前的钩子函数， 若返回 false  或者返回被 reject 的 Promise，则阻止切换。 -->
        <el-tabs :tab-position="tabPosition" class="demo-tabs" v-model="active" :before-leave="beforeLeave">
            <!-- 当我点击第一个tab的时候，active的值根据name绑定会变成0，然后就会对应step-item的第一个step，也就是基本信息 -->

            <!-- model-value / v-model	绑定值，选中选项卡的 name，默认值是第一个 tab 的 name -->
            <!-- name	与选项卡绑定值 value 对应的标识符，表示选项卡别名。默认值是tab面板的序列号，如第一个 tab 是 0 ,给个:就是变化字符串-->
            <el-form :model="addForm" ref="addFormRef" :rules="addFormRules">
                <el-tab-pane label="基本信息" :name="0">
                    <!--prop为 model 的键名 ,意思数据就是model-->
                    <el-form-item label="商品名称" prop="name">
                        <el-input v-model="addForm.name" placeholder="请输入商品名称" />
                    </el-form-item>
                    <el-form-item label="商品价格" prop="price">
                        <el-input v-model="addForm.price" placeholder="请输入商品价格" />
                    </el-form-item>
                    <el-form-item label="商品库存" prop="number">
                        <el-input v-model="addForm.number" placeholder="请输入商品库存" />
                    </el-form-item>
                    <el-form-item label="商品权重" prop="weight">
                        <el-input v-model="addForm.weight" placeholder="请输入商品权重" />
                    </el-form-item>
                    <el-form-item label="商品分类" style="margin-left: 10px;">
                        <el-cascader :options="options.data" :props="props" clearable separator=" > "
                            v-model="options.selectID" @change="ChangeSelect" style="width: 300px;" />

                    </el-form-item>
                </el-tab-pane>
                <el-tab-pane label="商品静态属性" :name="1">
                    <el-form-item :label="s.name" v-for="s in attrData.static" :key="s.id">
                        <el-input v-model="s.value" />
                    </el-form-item>

                </el-tab-pane>
                <el-tab-pane label="商品动态属性" :name="2">
                    <el-form-item :label="d.name" v-for="d in attrData.dynamic" :key="d.id">
                        <el-checkbox-group v-model="d.value">
                            <el-checkbox :label="v" name="type" v-for="(v,i) in d.value" :key="i" border></el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                </el-tab-pane>
                <el-tab-pane label="商品图片" :name="3">
<!-- action属性指定上传的地址,请求的yrl,on-preview属性指定点击文件时的预览处理函数,on-remove属性指定文件移除时的处理函数,list-type属性指定文件列表的类型   -->
                    <el-upload v-model:file-list="fileList" 
                        name="img"
                        :action="base.baseUrl + base.upload_img"
                        list-type="picture" :on-success="handleSuccess" :on-remove="handleRemove" :on-preview="handlePreview">
                        <el-button type="primary">上传图片</el-button>

                    </el-upload>

                </el-tab-pane>

<!-- 这个EditorComponent是我自己写的富文本编辑器组件，这个onDataEvent属性是我自己定义的事件，用来获取富文本编辑器的数据，下面用getDataHandler来接收这个事件 -->
                <el-tab-pane label="商品内容" :name="4">
                    <EditorComponent  ref="editorComponentRef" @onDataEvent="getDataHandler"/>
                    <el-button type="primary" @click="submitForm">提交</el-button>
                </el-tab-pane>
            </el-form>
        </el-tabs>
    </el-card>
    <el-dialog title="图片预览" v-model="PredialogVisible" width="50%">
        <img :src="preImgUrl" class="preview-img ">
    </el-dialog>

</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { ref, reactive, onMounted } from 'vue'
import api from '@/api/index'
import { ElMessage } from 'element-plus';
import base from '@/api/base'
import EditorComponent from '@/components/EditorComponent.vue';
import { useRouter } from 'vue-router'

const router = useRouter()

const tabPosition = ref('left')

const active = ref(0)

const options = reactive({
    data: [],
    selectID: null,
})

const props = {
    value: 'id',
    label: 'name',
    expandTrigger: 'hover',//鼠标滑上去展示下一级

}
//定义一个值来存储属性
const attrData = reactive({
    static: [],
    dynamic: [],
})



const addForm = reactive({
    name: '',
    price: '',
    number: '',
    weight: '',
    cid_one: '',
    cid_two: '',
    cid_three: '',
    pics: [],
    content: '',//这个content是富文本编辑器的内容
    attrs_static: [],
    attrs_dynamic: [],



})
const addFormRules = {
    name: [
        { required: true, message: '请输入商品名称', trigger: 'blur' },

    ],
    price: [
        { required: true, message: '请输入商品价格', trigger: 'blur' },
        { type: 'number', message: '请输入正确的价格', trigger: 'blur' ,transform: (value) => {return Number(value)}}//输入的值转为数字
    ],
    number: [
        { required: true, message: '请输入商品库存', trigger: 'blur' },
        { type: 'number', message: '请输入正确的库存', trigger: 'blur' ,transform: (value) => {return Number(value)}}
    ],
    weight: [
        { required: true, message: '请输入商品权重', trigger: 'blur' },
        { type: 'number', message: '请输入正确的权重', trigger: 'blur',transform: (value) => {return Number(value)}}
    ]

}
const addFormRef = ref(null)


//定义一个上传图片的数据对象
const fileList = ref([

])

let PredialogVisible = ref(false)
//定义一个图片预览地址
let preImgUrl = ref('')

const ChangeSelect = (value) => {
   //value是props里面的value，所以value就是props.value，也就是id,然后props的值来自于options.data，
   //所以value就是options.data的id,然后这个options.data就是请求里面的json数据,这个json数据又是后端在获取数据库的值后传过来的
   //三个都一样
    // console.log(value);
    // console.log(options.selectID)
    // console.log(options.data[0].id)
   
    //判断用户是否选择了商品分类
    if(options.selectID){//这个options.selectID是v-model又是props
        //判断选择的分类是否是最后一级
        if(options.selectID.length == 3){
            addForm.cid_one = options.selectID[0]
            addForm.cid_two = options.selectID[1]
            addForm.cid_three = options.selectID[2]
        }
        console.log(addForm)

    }

    //更新表单的分类id

}

onMounted(() => {
    get_category_list()
})

//获取商品分类数据
const get_category_list = () => {
    api.get_category_list(3).then(res => {
        console.log(res.data)
        options.data = res.data.data
    })
}
//未选择级联则无法切换到下一个tab
const beforeLeave = (activeName, oldActiveName) => {
    //判断是否选择了第三级分类
    if(options.selectID && options.selectID.length == 3){
        get_attr(options.selectID[2],'static')
        get_attr(options.selectID[2], 'dynamic')
        return true
    }
    ElMessage({
        'type': 'error',
        'message': '请选择商品分类'
    })
    return false

}

//获取属性
const get_attr = (selectKey, _type) => {
    //console.log('级联变化调用')
    if (_type === 'static'){
        api.get_attr_by_category(selectKey,_type).then(res => {
            attrData.static = res.data.data
            //console.log(attrData.static)
           
        })
    }else{
        api.get_attr_by_category(selectKey,_type).then(res => {
            //打印动态属性列表
            //console.log('动态属性列表===>',res)
            //遍历动态属性列表，将value值转换为数组
            res.data.data.forEach(item => {
                item.value = item.value ? item.value.split(','):[]//例如：'1,2,3'转换为[1,2,3]
            })

            attrData.dynamic = res.data.data
          
        })
    }
}
//上传图片成功的回调函数
const handleSuccess = (res, file, fileList) => {
    console.log(res)
    // console.log(file)
    // console.log(fileList)
    if (res.status === 200) {
        ElMessage({
            'type': 'success',
            'message': '上传成功'
        })
        //将图片添加到表单的pics数组中
        addForm.pics.push(res.data.path)

    }else{
        ElMessage({
            'type': 'error',
            'message': '上传失败'
        })
    }

}
//定义删除图片的回调函数
const handleRemove = (file, fileList) => {
    //console.log(file)//里面有file对象,res和url,status,message等属性
    //console.log('删除前',addForm.pics)
    //要删除的图片的pathd的索引
    let index = addForm.pics.indexOf(file.response.data.url)
    //用splice删除图片
    addForm.pics.splice(index, 1)//,索引和删除数量

    //console.log('删除后',addForm.pics)
    ElMessage({
        'type': 'info',
        'message': '已删除'
    })
}

//定义预览图片的回调函数


const handlePreview = (file) => {
   
    preImgUrl.value = file.response.data.url
    PredialogVisible.value = true
}

//定义获取富文本编辑器数据的方法
const getDataHandler = (data) => {
    console.log(data)
    //把富文本编辑器的数据赋值给表单的content字段
    addForm.content = data
}
// 在 setup 中定义 editorComponentRef
const editorComponentRef = ref(null);

//把表单数据提交到后端
const submitForm = () => {
    //将属性信息绑定到表单
    addForm.attrs_static=attrData.static
    addForm.attrs_dynamic=attrData.dynamic
    console.log(addForm)
    //提交表单
    api.add_product(addForm).then(res => {
        console.log(res)
        if (res.data.status === 200) {
            ElMessage({
                'type': 'success',
                'message': res.data.msg
            })
            //清空表单
            addFormRef.value.resetFields()
            //清空图片列表
            fileList.value = []
            // 清空富文本编辑器的内容
            if (editorComponentRef.value) {
                // 正确的方式是不直接操作editorComponentRef.value
                // 而是调用编辑器组件内部的方法或让它监听值的变化
                addForm.content = ''; // 只需重置内容值即可
            }
            //清空分类选择
            options.selectID = null
            //清空属性数据
            attrData.static = []
            attrData.dynamic = []
            //关闭弹窗
            PredialogVisible.value = false
            //跳转到商品列表页面
            router.push('/product_list/')
        } else {
            ElMessage({
                'type': 'error',
                'message': res.data.msg
            })
        }
        })
}

</script>

<style scoped>
.box-card {
    margin-top: 20px;
}

.demo-tabs {
    margin-top: 30px;
}

.preview-img {
    width: 100%;
}

/* 添加以下样式来优化TinyMCE在小屏幕上的显示 */
:deep(.tox-tinymce) {
    max-width: 100%;
    overflow: hidden;
}

:deep(.tox-editor-container) {
    display: flex;
    flex-direction: column;
}

:deep(.tox-toolbar) {
    flex-wrap: wrap;
}

/* 在小屏幕上适应性调整 */
@media (max-width: 768px) {
    :deep(.tox-toolbar__group) {
        flex-wrap: wrap;
    }
}
</style>