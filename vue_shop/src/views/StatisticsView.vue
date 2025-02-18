<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>数据统计</el-breadcrumb-item>
        <el-breadcrumb-item>统计列表</el-breadcrumb-item>

    </el-breadcrumb>

    <div id="chart3" class="chart"></div>

    <div class="charts">
        <div id="chart1"></div>
        <div id="chart2"></div>
        <div id="chart"></div>


    </div>


</template>

<script setup>
//面包屑的图标,搜索按钮的图标
import { ArrowRight } from '@element-plus/icons-vue'
import { getCurrentInstance ,onMounted} from 'vue';//获取当前实例也就是全局定义的插件，,app.config.globalProperties.$echarts = (element) => {}
import api from '@/api/index'


// 定义图表插件，获取当前实例
const { proxy}= getCurrentInstance();
// 定义图表数据
let option = {
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            data: [150, 230, 224, 218, 135, 147, 260],
            type: 'bar'
        }
    ]
}

let option1 = {
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '60%'],
      avoidLabelOverlap: false,
      padAngle: 5,
      itemStyle: {
        borderRadius: 10
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' }
      ]
    }
  ]
};

let option2 = {
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            data: [150, 230, 224, 218, 135, 147, 260],
            type: 'line'
        }
    ]
}

let option3 = {
  title: {
    text: '分类统计'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    backgroundColor: '#fff', // 背景色
    
  },
  legend: {},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    boundaryGap: [0, 0.01]
  },
  yAxis: {
    type: 'category',
    data: ['Brazil', 'Indonesia', 'USA', 'India', 'China', 'World']
  },
  series: [
    {
      name: '商品分类',
      type: 'bar',
      data: [18203, 23489, 29034, 104970, 131744, 630230]
    },
   
  ]
};



onMounted(() => {
    getDataCategory()
    // 调用定义的图表插件
    //proxy.$echarts('chart',option)不能在这里在渲染了，因为这个不会等getDataCategory()执行完毕，而是直接渲染，所以是之前的数据，所以我们索性直接在获取的时候渲染
    //proxy.$echarts('chart1',option1)
    //proxy.$echarts('chart2',option)
    //proxy.$echarts('chart3',option3)
})
//获取数据分类
const getDataCategory =()=>{
    api.get_category_statistics().then(res => {
        console.log(res)
        //更新option的数据
        option.series[0].data =res.data.data.series//[17, 49, 89]
        option.xAxis.data = res.data.data.xAxis//['1级分类', '2级分类', '3级分类']
        //重新渲染
        proxy.$echarts('chart',option)

        //更新option1的数据
        option1.series[0].data = res.data.data.series.map((value, index) => {
          return {
            
            value: value,
            name: res.data.data.xAxis[index]
          };
        });
        //重新渲染
        proxy.$echarts('chart1',option1)

        //更新option2的数据
        option2.series[0].data =res.data.data.series//[17, 49, 89]
        option2.xAxis.data = res.data.data.xAxis//['1级分类', '2级分类', '3级分类']
        //重新渲染
        proxy.$echarts('chart2',option2)

        //更新option3的数据
        option3.series[0].data = res.data.data.series//[17, 49, 89]
        option3.yAxis.data = res.data.data.xAxis//['1级分类', '2级分类', '3级分类']
        //重新渲染
        proxy.$echarts('chart3',option3)
        
    })

}


</script>

<style scoped>
.chart {
    width: 100%;
    height: 500px;
    margin-top: 20px;
    background-color: #f5f5f5;

}

.charts {
    display: flex;
    justify-content: space-between; /* 修改为两端对齐 */
}

.charts div {

    flex: 1;
    height: 300px;
    margin-top: 20px;
    background-color: #f5f5f5;
    margin-right: 15px; /* 添加右边间隔 */
}

/* 去掉最后一个 div 的右边间隔 */
.charts div:last-child {
    margin-right: 0;
}

</style>