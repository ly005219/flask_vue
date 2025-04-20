import * as echarts from 'echarts'

export default {
    // echarts作为全局变量
    install(app) {
        // 存储图表实例的Map，以元素ID为键
        const chartInstances = new Map()
        
        // 配置全局变量, element代表将图表渲染到哪个元素上
        app.config.globalProperties.$echarts = (element, option) => {
            const dom = document.getElementById(element)
            if (!dom) {
                console.error(`Element with id '${element}' not found.`)
                return
            }
            
            let myChart
            
            // 检查是否已存在该元素的图表实例
            if (chartInstances.has(element)) {
                // 如果存在，则获取现有实例
                myChart = chartInstances.get(element)
                // 清除旧的配置
                myChart.clear()
            } else {
                // 如果不存在，创建新实例
                myChart = echarts.init(dom)
                // 将新实例存储到Map中
                chartInstances.set(element, myChart)
                
                // 添加窗口大小变化时的自适应调整
                window.addEventListener('resize', () => {
                    myChart.resize()
                })
            }
            
            // 设置新的配置
            myChart.setOption(option)
            
            // 返回图表实例，以便进一步操作
            return myChart
        }
        
        // 添加销毁图表的方法
        app.config.globalProperties.$disposeEcharts = (element) => {
            if (chartInstances.has(element)) {
                const chart = chartInstances.get(element)
                chart.dispose()
                chartInstances.delete(element)
            }
        }
    }
}


