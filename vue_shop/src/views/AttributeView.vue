<template>

    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>属性列表</el-breadcrumb-item>

    </el-breadcrumb>


    <el-card class="box-card">

        <el-alert title="分类属性只可以选择最后一级分类，请注意！" type="warning" effect="dark" style="margin-bottom: 10px;" />
        <div>
            <span class="attr-title">选择分类</span>
            <el-cascader :options="options.data" :props="props" clearable separator=" > " class="cascader"
                v-model="options.selectID" @change="ChangeSelect" />

        </div>

        <div>
            <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
                <el-tab-pane label="静态属性" name="static">
                    <el-button type="primary" :icon="CirclePlus" style="margin-bottom: 10px;"
                        @click="addDialogVisible = true" :disabled="isButtonShow">添加属性</el-button>
                    <el-table :data="attrData.static" border >

                        <el-table-column type="index"></el-table-column>
                        <el-table-column prop="name" label="属性名称" width="180"></el-table-column>
                        <el-table-column prop="value" label="属性值" width="180"></el-table-column>

                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button type="success" @click="editStaticClick(scope.$index,scope.row)">编辑</el-button>
                                <el-button type="danger" @click="deleteAttr(scope.$index,scope.row)">删除</el-button>
                            </template>
                        </el-table-column>

                    </el-table>



                </el-tab-pane>
                <el-tab-pane label="动态属性" name="dynamic" @tab-click="handleClick">
                    <el-button type="primary" :icon="CirclePlus" style="margin-bottom: 10px;"
                        @click="addDialogVisible = true" :disabled="isButtonShow">添加属性</el-button>
                    <el-table :data="attrData.dynamic" border>
                        <!-- 展开行 -->
                        <el-table-column type="expand">
                            <template #default="scope">
                                <el-tag v-for="(v, index) in scope.row.value" style="margin: 5px;" closable @close="closeTag(scope.row.id,scope.row.value,index)">{{ v }}</el-tag>
                                <TagComponent @addTagEvent="getTagValue" :row="scope.row" ></TagComponent>
                            </template>
                        </el-table-column>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column prop="name" label="属性名称" width="180"></el-table-column>

                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button type="success" @click="editClick(scope.$index,scope.row)">编辑</el-button>
                                <el-button type="danger" @click="deleteAttr(scope.$index,scope.row)">删除</el-button>
                            </template>
                        </el-table-column>

                    </el-table>



                </el-tab-pane>

            </el-tabs>


           


        </div>
    </el-card>

    <!-- 新增属性弹窗 -->
    <el-dialog v-model="addDialogVisible" :title="_type === 'dynamic' ? '添加动态属性' : '添加静态属性'" @close="resetForm">

        <el-form :model="addForm" :rules="addFormRules" ref="addFormRef">


            <el-form-item label="属性名称" prop="name">
                <el-input v-model="addForm.name" placeholder="请输入属性名称"></el-input>
            </el-form-item>



            <el-form-item>
                <el-button type="primary" @click="addAttr">
                    确定
                </el-button>
                <el-button @click="resetForm('addFormRef')">取消</el-button>
            </el-form-item>

        </el-form>

    </el-dialog>

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

</template>




<script setup>
import { ArrowRight,CirclePlus } from '@element-plus/icons-vue'
import { reactive , onMounted ,ref,watch,computed, nextTick } from 'vue';
import api from '@/api/index'
import TagComponent from '@/components/TagComponent.vue';//直接把他当作标签引用



const options =reactive({
    data: [],
    selectID: null,

})


const props = {
    value: 'id',
    label: 'name',
    expandTrigger: 'hover',//鼠标滑上去展示下一级
   

}

const flag=reactive({
    static: false,//静态属性不可以获取
    dynamic: false,

})


const activeName = ref('static')//默认显示静态属性

const attrData = reactive({
    static: [],
    dynamic: [],
})

let addDialogVisible = ref(false)//新增属性弹窗的显示状态,不要打开页面就显示,点击按钮在显示
const addForm = reactive({
    name: '',
 

})
let addFormRules = reactive({//对应上面的props
    name: [
        { required: true, message: '请输入属性名称', trigger: 'blur' },
        { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' },
        {trigger: 'change'}, // ，当用户在输入框中输入内容并离开输入框时，会触发验证。
    ],



})
const addFormRef = ref(null)

//让新增属性按钮仅在选择级联分类在显示
let isButtonShow = computed(() => {
    if (options.selectID && options.selectID.length === 3) {
        return false
        } else {
            return true//禁用
    }
    })

//取消后重置
const resetForm = () =>{
   
    addFormRef.value.resetFields()
    addDialogVisible.value = false
}

// 监听 addDialogVisible，关闭时重置表单
// watch(addDialogVisible, (newVal) => {
//     if (!newVal) {
//         resetForm();
//     }
// });
const _type = ref('')//新增属性的类型，默认是静态属性

const handleClick = (tab, event) => {
    //console.log('下面是tab')
    //console.log(tab, event)
    if (tab.props.name === 'static'){
        _type.value = 'static'
    }else{
        _type.value = 'dynamic'
    }
  //console.log(options.selectID)//当前选择的分类ID，123级都会有
  if(options.selectID){
    if(options.selectID.length === 3){
        //console.log('级联选择手动调用')
        let selectKey = options.selectID[2]
        let _type=tab.props.name
         //根据flag标识，判断是否可以获取属性数据
        // if(_type === 'static'){
        //     if(flag.static){
        //         api.get_attr_by_category(selectKey,_type).then(res => {
        //             console.log(res)
        //             attrData.static = res.data.data
        //         })
        //     }
        // }else{
        //     if(flag.dynamic){
        //         api.get_attr_by_category(selectKey,_type).then(res => {
        //             console.log(res)
        //             attrData.dynamic = res.data.data
        //         })
        //     }
        // }
        get_attr_by_category(selectKey,_type)
    }else{
        attrData.static = []
        attrData.dynamic = []
    }


       
           
        }
    }
  
//级联选择器的change函数，值发生变化的时候就触发，以便我调用接口加载数据
const ChangeSelect = (val) => {
   // console.log('下面的是val')
    //console.log(val)//就是这个分类的ID数组，也就是级联的props的value值，id  //等同于console.log(options.selectID)
    //静态和动态属性可以获取


    if(val){ 
        if(val.length === 3){
            let selectKey = val[2]
            let _type=activeName.value
            flag.static = true
            flag.dynamic = true
            // api.get_attr_by_category(selectKey,_type).then(res => {
            //     console.log(res)
            //     if(_type === 'static'){
            //         attrData.static = res.data.data
            //         //静态属性不可以获取，因为数据没有变更
            //         flag.static = false

            //     }else{
            //         attrData.dynamic = res.data.data
            //         //动态属性不可以获取，因为数据没有变更
            //         flag.dynamic = false
            //     }
            // })
            get_attr_by_category(selectKey,_type)
    }else{//清空二级和三级分类的属性列表
        attrData.static = []
        attrData.dynamic = []
    }
   
    }else{
        attrData.static = []
        attrData.dynamic = []
    }
  }




const get_attr_by_category = (selectKey, _type) => {
   // console.log('级联变化调用')
    if (_type === 'static'){
        api.get_attr_by_category(selectKey,_type).then(res => {
            attrData.static = res.data.data
            flag.static = false
            //console.log(attrData.static)
        })
    }else{
        api.get_attr_by_category(selectKey,_type).then(res => {
            //打印动态属性列表
           // console.log('动态属性列表===>',res)
            //遍历动态属性列表，将value值转换为数组
            res.data.data.forEach(item => {
                item.value = item.value ? item.value.split(','):[]//例如：'1,2,3'转换为[1,2,3]
            })

            attrData.dynamic = res.data.data
            flag.dynamic = false
           // console.log(attrData.dynamic)
        })
    }
}




onMounted(() => {
    get_category_list()
    
})


const get_category_list = () => {
    api.get_category_list(3).then(res => {
       // console.log(res.data)
        options.data = res.data.data
    }) 
}

//确定按钮调用增加属性接口
const addAttr = () => {


    //console.log(activeName.value)
    //console.log(options.selectID)
    let params = {
        "name": addForm.name,
        "category_id": options.selectID[2],
        "_type": activeName.value,


    }
    
    api.add_attr(params).then(res => {
       // console.log(res)
        if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })


            if (_type.value === 'dynamic') {
                attrData.dynamic.push(res.data.data)
            } else {
                attrData.static.push(res.data.data)
            }
            get_attr_by_category(options.selectID[2],activeName.value)
            addDialogVisible.value = false
        } else {
            ElMessage.warning({
                showClose: true,
                message: res.data.msg});

                }
        
            
        



    })
}

//
const getTagValue = (value) => {//这个value就是前面子组件,emit传过来的值
  //  console.log(value.inputValue,value.row.id,activeName.value)
   // console.log(value.row._type)
    //将新输入的值添加到原来的数组中,这样我就将原来的值和现在的值加在一起了,然后在调用put也就等同于增加新属性值了
    value.row.value.push(value.inputValue)//这个value.row.value是一个列表


    let params = {
      
        "_type": value.row._type,
        "value": value.row.value.join(','),//将列表转换为字符串，例如：[1,2,3]转换为'1,2,3'

    
    }
    api.updata_attr_value(value.row.id,params).then(res => {
      //  console.log(res)
        ElMessage({
        type: 'success',
        message: res.data.msg,
    });


        //刷新属性列表
        get_attr_by_category(options.selectID[2],activeName.value)
    })
}

const closeTag = (id,valueList,index) => {
   // console.log(id,valueList,index)//要更新的id,要更新的值列表,要删除的索引
    //在列表中删除指定的数据,这个id是table的:data值的id,index是当前行数据的第几个值
    valueList.splice(index,1)//删除一个元素
   // console.log(valueList)
    let params = {
        "value": valueList.join(','),
        }
    api.updata_attr_value(id,params).then(res => {
        console.log(res)
        ElMessage({
        type: 'success',
        message: res.data.msg,
        }
        )
    })

    }

//删除属性
const deleteAttr = (index,row) => {
    //console.log(index)
    
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

                   // console.log(res)
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

//修改静态属性
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

</script>


<style scoped>
.box-card {
    margin-top: 20px;
}
.attr-title {
    margin-right:10px ;

}
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

</style>