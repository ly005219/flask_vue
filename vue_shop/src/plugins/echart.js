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
                try {
                    myChart = chartInstances.get(element)
                    // 检查图表实例是否有效
                    if (!myChart.isDisposed()) {
                        // 清除旧的配置
                        myChart.clear()
                    } else {
                        // 如果已被销毁，则创建新实例
                        chartInstances.delete(element)
                        myChart = echarts.init(dom)
                        chartInstances.set(element, myChart)
                    }
                } catch (e) {
                    // 出错时重新创建图表实例
                    try {
                        chartInstances.delete(element)
                        myChart = echarts.init(dom)
                        chartInstances.set(element, myChart)
                    } catch (err) {
                        console.debug('图表重新初始化失败', err)
                        return null
                    }
                }
            } else {
                // 如果不存在，创建新实例
                try {
                    myChart = echarts.init(dom)
                    // 将新实例存储到Map中
                    chartInstances.set(element, myChart)
                } catch (err) {
                    console.debug('图表初始化失败', err)
                    return null
                }
            }
            
            // 添加窗口大小变化时的自适应调整
            const resizeHandler = () => {
                if (myChart && !myChart.isDisposed()) {
                    myChart.resize()
                }
            }
            
            // 移除旧的resize监听器以避免重复
            window.removeEventListener('resize', resizeHandler)
            window.addEventListener('resize', resizeHandler)
            
            // 设置新的配置
            try {
                myChart.setOption(option)
            } catch (err) {
                console.debug('设置图表配置失败', err)
            }
            
            // 返回图表实例，以便进一步操作
            return myChart
        }
        
        // 添加销毁图表的方法
        app.config.globalProperties.$disposeEcharts = (element) => {
            if (chartInstances.has(element)) {
                try {
                    const chart = chartInstances.get(element)
                    if (chart && !chart.isDisposed()) {
                        chart.dispose()
                    }
                    chartInstances.delete(element)
                } catch (err) {
                    console.debug('销毁图表失败', err)
                    chartInstances.delete(element)
                }
            }
        }
        
        // 在组件卸载时自动清理图表实例
        app.mixin({
            beforeUnmount() {
                // 清理属于这个组件的所有图表实例
                chartInstances.forEach((chart, id) => {
                    try {
                        if (chart && !chart.isDisposed()) {
                            chart.dispose()
                            chartInstances.delete(id)
                        }
                    } catch (e) {
                        // 静默处理错误
                        chartInstances.delete(id)
                    }
                })
            }
        })
    }
}


