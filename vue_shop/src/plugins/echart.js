import * as echarts from 'echarts'


export default {
    // echarts作为全局变量
    install(app) { // 这里的修改
        // 配置全局变量, element代表将图表渲染到哪个元素上
        app.config.globalProperties.$echarts = (element,option) => {
            // 实例化echarts对象
            let myChart = echarts.init(document.getElementById(element))
            // 创建图表需要显示的数据

            myChart.setOption(option);
        }
    }
}


