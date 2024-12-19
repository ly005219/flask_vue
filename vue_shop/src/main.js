import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import elementIcon from './plugins/icons'
import echart from './plugins/echart'


createApp(App).use(router).use(elementIcon).use(echart).mount('#app')
