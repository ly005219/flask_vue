<template>
    <!-- 新增标签 -->
     <!--  -->
    <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="input-new-tag" size="small"
         @blur="handleInputConfirm" />
    <el-button v-else class="button-new-tag" size="small" @click="showInput">
        + New Tag
    </el-button>


</template>

<script setup>

import { ref, nextTick } from 'vue'

const inputValue = ref('')

const inputVisible = ref(false)
const InputRef = ref(null)
const emit=defineEmits(['addTagEvent'])//定义一个自定义事件，用来触发父组件的addTagEvent事件
//定义父组件传递过来的值
const props=defineProps({
    row:{
        type:Object,//传递过来的数据类型
        default:()=>Object//默认值
    }
})

const showInput = () => {
    inputVisible.value = true//显示输入框
    nextTick(() => {
        InputRef.value.input.focus()//聚焦到输入框
    })
}
//丢失焦点或者回车
const handleInputConfirm = () => {
    //触发事件'
    emit('addTagEvent',{'inputValue':inputValue.value,'row':props.row})
    //console.log('输入框内容：', inputValue.value)
    inputVisible.value = false
    inputValue.value = ''
}

</script>

<style scoped>
.input-new-tag {
    width: 100px;
}
</style>