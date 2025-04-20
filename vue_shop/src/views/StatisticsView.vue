<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>数据统计</el-breadcrumb-item>
        <el-breadcrumb-item>统计列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 统计视图切换器 -->
    <div class="chart-tabs">
      <el-radio-group v-model="activeChartType" @change="handleChartTypeChange">
        <el-radio-button value="category">分类统计</el-radio-button>
        <el-radio-button value="user">用户统计</el-radio-button>
        <el-radio-button value="product">商品销量</el-radio-button>
        <el-radio-button value="order">订单数据</el-radio-button>
        <el-radio-button value="stock">库存数据</el-radio-button>
      </el-radio-group>
      
      <div class="date-filter" v-if="activeChartType !== 'category'">
        <el-select v-model="dateRange" placeholder="选择时间范围" @change="handleDateRangeChange" teleported popper-append-to-body>
          <el-option label="最近7天" value="7"></el-option>
          <el-option label="最近30天" value="30"></el-option>
          <el-option label="最近90天" value="90"></el-option>
          <el-option label="今年" value="year"></el-option>
          <el-option label="全部" value="all"></el-option>
        </el-select>
      </div>
    </div>

    <!-- 主统计图表 -->
    <div id="mainChart" class="chart"></div>

    <!-- 次要统计图表 -->
    <div class="charts">
        <div id="chart1"></div>
        <div id="chart2"></div>
        <div id="chart3"></div>
    </div>
</template>

<script setup>
//面包屑的图标,搜索按钮的图标
import { ArrowRight } from '@element-plus/icons-vue'
import { getCurrentInstance, onMounted, onBeforeUnmount, ref, reactive, nextTick } from 'vue';//获取当前实例也就是全局定义的插件
//import { ElMessage } from 'element-plus'
import api from '@/api/index'

// 当前激活的图表类型
const activeChartType = ref('category')
// 日期范围选择
const dateRange = ref('30')

// 定义图表插件，获取当前实例
const { proxy } = getCurrentInstance();
const message = proxy.$message || console.log; // 使用安全的消息方法或降级为console.log

// 图表ID数组，用于组件销毁时清理
const chartIds = ['mainChart', 'chart1', 'chart2', 'chart3']

// 定义图表数据
const chartOptions = reactive({
  // 分类统计图表
  category: {
    main: {
      title: {
        text: '商品分类统计'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        backgroundColor: '#fff',
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
        data: ['一级分类', '二级分类', '三级分类']
      },
      series: [
        {
          name: '商品分类',
          type: 'bar',
          data: [18, 49, 89]
        }
      ]
    },
    pie: {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        top: '5%',
        left: 'center'
      },
      series: [
        {
          name: '分类占比',
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
            { value: 18, name: '一级分类' },
            { value: 49, name: '二级分类' },
            { value: 89, name: '三级分类' }
          ]
        }
      ]
    },
    line: {
      xAxis: {
        type: 'category',
        data: ['一级分类', '二级分类', '三级分类']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: [18, 49, 89],
          type: 'line',
          smooth: true
        }
      ]
    },
    bar: {
      xAxis: {
        type: 'category',
        data: ['一级分类', '二级分类', '三级分类']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: [18, 49, 89],
          type: 'bar'
        }
      ]
    }
  },
  
  // 用户统计图表
  user: {
    main: {
      title: {
        text: '用户注册趋势'
      },
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '新增用户',
          type: 'line',
          smooth: true,
          data: [10, 15, 20, 25, 30, 35, 40],
          itemStyle: {
            color: '#409EFF'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(64,158,255,0.6)' },
                { offset: 1, color: 'rgba(64,158,255,0.1)' }
              ]
            }
          }
        }
      ]
    },
    pie: {
      title: {
        text: '用户角色分布'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'horizontal',
        bottom: 'bottom'
      },
      series: [
        {
          name: '角色分布',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 60, name: '普通用户' },
            { value: 20, name: '管理员' },
            { value: 10, name: '超级管理员' },
            { value: 5, name: '测试账号' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    },
    bar: {
      title: {
        text: '用户活跃度'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '活跃用户',
          type: 'bar',
          data: [120, 200, 150, 80, 70, 110, 130]
        }
      ]
    }
  },
  
  // 商品销量统计
  product: {
    main: {
      title: {
        text: '热门商品销量Top10'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value'
      },
      yAxis: {
        type: 'category',
        data: ['商品1', '商品2', '商品3', '商品4', '商品5', '商品6', '商品7', '商品8', '商品9', '商品10'].reverse(),
        axisLabel: {
          formatter: function(value) {
            if (value.length > 8) {
              return value.substring(0, 8) + '...';
            }
            return value;
          }
        }
      },
      series: [
        {
          name: '销量',
          type: 'bar',
          data: [320, 302, 301, 290, 270, 260, 230, 210, 190, 180].reverse(),
          itemStyle: {
            color: function(params) {
              // 根据销量数值生成不同深浅的颜色
              const colorList = [
                '#83bff6', '#188df0', '#188df0', '#188df0', '#188df0',
                '#2378f7', '#2378f7', '#2378f7', '#005eaa', '#005eaa'
              ];
              return colorList[params.dataIndex];
            }
          }
        }
      ]
    },
    pie: {
      title: {
        text: '各类商品销量占比'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        type: 'scroll',
        orient: 'horizontal',
        bottom: 'bottom'
      },
      series: [
        {
          name: '销量占比',
          type: 'pie',
          radius: '55%',
          center: ['50%', '45%'],
          data: [
            { value: 335, name: '电子产品' },
            { value: 310, name: '服装服饰' },
            { value: 234, name: '家居用品' },
            { value: 135, name: '食品饮料' },
            { value: 148, name: '图书音像' }
          ]
        }
      ]
    },
    line: {
      title: {
        text: '商品销量趋势'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['电子产品', '服装服饰', '家居用品']
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '电子产品',
          type: 'line',
          data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
          name: '服装服饰',
          type: 'line',
          data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
          name: '家居用品',
          type: 'line',
          data: [150, 232, 201, 154, 190, 330, 410]
        }
      ]
    }
  },
  
  // 订单统计
  order: {
    main: {
      title: {
        text: '订单数量趋势'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['订单数', '销售额']
      },
      xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
      },
      yAxis: [
        {
          type: 'value',
          name: '订单数',
          axisLabel: {
            formatter: '{value} 单'
          }
        },
        {
          type: 'value',
          name: '销售额',
          position: 'right',
          axisLabel: {
            formatter: '{value} 元'
          }
        }
      ],
      series: [
        {
          name: '订单数',
          type: 'bar',
          data: [320, 332, 301, 334, 390, 330, 320]
        },
        {
          name: '销售额',
          type: 'line',
          yAxisIndex: 1,
          data: [82000, 93200, 90100, 93400, 109000, 133000, 132000]
        }
      ]
    },
    pie: {
      title: {
        text: '订单状态分布'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'horizontal',
        bottom: 'bottom'
      },
      series: [
        {
          name: '订单状态',
          type: 'pie',
          radius: '55%',
          data: [
            { value: 335, name: '已完成', itemStyle: { color: '#67C23A' } },
            { value: 310, name: '待付款', itemStyle: { color: '#E6A23C' } },
            { value: 234, name: '待发货', itemStyle: { color: '#409EFF' } },
            { value: 135, name: '待收货', itemStyle: { color: '#F56C6C' } },
            { value: 148, name: '已取消', itemStyle: { color: '#909399' } }
          ]
        }
      ]
    },
    line: {
      title: {
        text: '各时段订单量'
      },
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['0点', '3点', '6点', '9点', '12点', '15点', '18点', '21点']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: [10, 5, 7, 30, 45, 50, 60, 40],
          type: 'line',
          smooth: true,
          areaStyle: {}
        }
      ]
    }
  },
  
  // 库存统计
  stock: {
    main: {
      title: {
        text: '库存预警商品'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['当前库存', '安全库存']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value'
      },
      yAxis: {
        type: 'category',
        data: ['商品A', '商品B', '商品C', '商品D', '商品E'].reverse()
      },
      series: [
        {
          name: '当前库存',
          type: 'bar',
          data: [12, 8, 5, 7, 3].reverse(),
          itemStyle: {
            color: function(params) {
              // 红绿配色根据是否低于安全库存
              const values = [12, 8, 5, 7, 3].reverse();
              const safeValues = [10, 10, 10, 10, 10].reverse();
              return values[params.dataIndex] < safeValues[params.dataIndex] ? '#F56C6C' : '#67C23A';
            }
          }
        },
        {
          name: '安全库存',
          type: 'line',
          data: [10, 10, 10, 10, 10].reverse(),
          itemStyle: {
            color: '#E6A23C'
          }
        }
      ]
    },
    pie: {
      title: {
        text: '库存分布情况'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'horizontal',
        bottom: 'bottom'
      },
      series: [
        {
          name: '库存占比',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: [
            { value: 60, name: '充足库存', itemStyle: { color: '#67C23A' } },
            { value: 25, name: '适中库存', itemStyle: { color: '#E6A23C' } },
            { value: 15, name: '低库存', itemStyle: { color: '#F56C6C' } }
          ]
        }
      ]
    },
    bar: {
      title: {
        text: '库存周转率'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      xAxis: {
        type: 'category',
        data: ['电子产品', '服装服饰', '家居用品', '食品饮料', '图书音像']
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}次/月'
        }
      },
      series: [
        {
          name: '周转率',
          type: 'bar',
          data: [3.2, 4.5, 2.8, 6.7, 1.9],
          itemStyle: {
            color: function(params) {
              // 颜色映射
              const colorList = ['#91cc75', '#fac858', '#ee6666', '#73c0de', '#5470c6'];
              return colorList[params.dataIndex % colorList.length];
            }
          }
        }
      ]
    }
  }
})

onMounted(() => {
  renderCharts('category')
})

// 组件销毁前清理所有图表实例
onBeforeUnmount(() => {
  // 清理所有图表实例
  chartIds.forEach(id => {
    if (proxy.$disposeEcharts) {
      proxy.$disposeEcharts(id)
    }
  })
})

// 处理图表类型变化
const handleChartTypeChange = (type) => {
  renderCharts(type)
}

// 处理日期范围变化
const handleDateRangeChange = (range) => {
  // 模拟根据日期范围获取数据
  message.info(`已切换到${range === 'year' ? '今年' : range === 'all' ? '全部' : `最近${range}天`}的数据`)
  // 使用nextTick确保DOM更新完成后再渲染图表
  nextTick(() => {
    renderCharts(activeChartType.value)
  })
}

// 渲染指定类型的图表
const renderCharts = (type) => {
  // 清除之前的图表实例以避免内存泄漏
  chartIds.forEach(id => {
    if (proxy.$disposeEcharts) {
      proxy.$disposeEcharts(id)
    }
  })
  
  // 使用nextTick确保DOM已准备好
  nextTick(() => {
    if (type === 'category') {
      // 对于分类统计，调用后端API获取真实数据
      getDataCategory()
    } else {
      // 对于其他统计，使用模拟数据
      renderMockCharts(type)
    }
  })
}

// 渲染模拟数据图表
const renderMockCharts = (type) => {
  // 确保清除之前的图表实例
  const charts = chartOptions[type]
  
  // 主图表
  proxy.$echarts('mainChart', charts.main)
  
  // 辅助图表 - 使用不同的图表类型
  if (charts.pie) {
    proxy.$echarts('chart1', charts.pie)
  }
  
  if (charts.line) {
    proxy.$echarts('chart2', charts.line)
  }
  
  if (charts.bar) {
    proxy.$echarts('chart3', charts.bar)
  }
  
  // 模拟API调用延迟
  setTimeout(() => {
    message.success(`${type === 'user' ? '用户' : type === 'product' ? '商品销量' : type === 'order' ? '订单' : '库存'}统计数据加载完成`)
  }, 500)
}

// 获取商品分类数据（实际API调用）
const getDataCategory = () => {
  api.get_category_statistics().then(res => {
    // console.log(res)
    // 更新图表数据
    chartOptions.category.main.series[0].data = res.data.data.series
    chartOptions.category.main.yAxis.data = res.data.data.xAxis
    
    // 更新饼图数据
    chartOptions.category.pie.series[0].data = res.data.data.series.map((value, index) => {
      return {
        value: value,
        name: res.data.data.xAxis[index]
      }
    })
    
    // 更新折线图数据
    chartOptions.category.line.series[0].data = res.data.data.series
    chartOptions.category.line.xAxis.data = res.data.data.xAxis
    
    // 更新柱状图数据
    chartOptions.category.bar.series[0].data = res.data.data.series
    chartOptions.category.bar.xAxis.data = res.data.data.xAxis
    
    // 渲染图表
    proxy.$echarts('mainChart', chartOptions.category.main)
    proxy.$echarts('chart1', chartOptions.category.pie)
    proxy.$echarts('chart2', chartOptions.category.line)
    proxy.$echarts('chart3', chartOptions.category.bar)
  }).catch(err => {
    console.error('获取分类统计数据失败', err)
    message.error('获取数据失败，显示模拟数据')
    
    // 加载失败时使用默认数据
    proxy.$echarts('mainChart', chartOptions.category.main)
    proxy.$echarts('chart1', chartOptions.category.pie)
    proxy.$echarts('chart2', chartOptions.category.line)
    proxy.$echarts('chart3', chartOptions.category.bar)
  })
}
</script>

<style scoped>
.chart-tabs {
  margin: 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-filter {
  margin-left: 20px;
}

#mainChart {
  width: 100%;
  height: 500px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.charts {
  display: flex;
  justify-content: space-between;
}

.charts div {
  flex: 1;
  height: 300px;
  background-color: #f9f9f9;
  margin-right: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.charts div:last-child {
  margin-right: 0;
}
</style>