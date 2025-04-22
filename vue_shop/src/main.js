import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import elementIcon from './plugins/icons'
import echart from './plugins/echart'
import safeMessage from './plugins/message'


// 添加ResizeObserver错误修复，完全静默处理错误
const originalResizeObserver = window.ResizeObserver;
if (originalResizeObserver) {
  // 保存原始的console.warn方法
  const originalConsoleWarn = console.warn;
  
  // 重写ResizeObserver类
  window.ResizeObserver = class ResizeObserver extends originalResizeObserver {
    constructor(callback) {
      const wrappedCallback = (entries, observer) => {
        // 在requestAnimationFrame中运行回调，避免无限循环
        window.requestAnimationFrame(() => {
          try {
            // 在try-catch中包装调用，以防DOM元素不存在
            callback(entries, observer);
          } catch (error) {
            // 完全屏蔽错误，不输出任何警告
            // 可以在开发环境下记录到其他地方，但不显示在控制台
            if (process.env.NODE_ENV === 'development') {
              // 仅在开发环境下，使用自定义格式记录到控制台
              console.debug('[已抑制的ResizeObserver错误]', error.message);
            }
          }
        });
      };
      super(wrappedCallback);
    }
    
    // 重写disconnect方法避免不必要的错误
    disconnect() {
      try {
        super.disconnect();
      } catch (error) {
        // 完全静默处理
      }
    }

    // 重写observe方法，增加错误处理
    observe(target) {
      try {
        super.observe(target);
      } catch (error) {
        // 静默处理observe错误
      }
    }

    // 重写unobserve方法，增加错误处理
    unobserve(target) {
      try {
        super.unobserve(target);
      } catch (error) {
        // 静默处理unobserve错误
      }
    }
  };
  
  // 重写console.warn，过滤掉ResizeObserver相关警告
  console.warn = function(...args) {
    // 如果警告与ResizeObserver相关，则完全忽略
    if (args.length > 0 && 
        (typeof args[0] === 'string' && 
         (args[0].includes('ResizeObserver') || 
          args[0].includes('getBoundingClientRect')))) {
      // 忽略这些警告
      return;
    }
    
    // 其他警告正常显示
    return originalConsoleWarn.apply(this, args);
  };
}

// 创建全局样式，确保消息显示正确
const globalStyle = document.createElement('style');
globalStyle.textContent = `
  .global-message {
    position: fixed !important;
    top: 20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    z-index: 9999 !important;
  }
`;
document.head.appendChild(globalStyle);

// 创建应用实例
const app = createApp(App);

// 使用插件
app.use(router).use(elementIcon).use(echart);

// 设置Element Plus全局配置
app.config.globalProperties.$ELEMENT = {
  size: 'default',
  zIndex: 3000,
  select: {
    teleported: true, // 确保所有Select组件都弹出到body
    popperAppendToBody: true
  },
  // 增加dialog组件的全局配置
  dialog: {
    teleported: true, // 确保dialog弹出到body
    appendToBody: true
  },
  // 增加date-picker组件的全局配置  
  datePicker: {
    teleported: true,
    popperAppendToBody: true
  },
  // 增加cascader组件的全局配置
  cascader: {
    teleported: true,
    popperAppendToBody: true
  },
  // 增加tooltip组件的全局配置
  tooltip: {
    teleported: true,
    popperAppendToBody: true,
    popperOptions: {
      strategy: 'fixed'
    }
  }
};

// 添加安全消息作为全局属性
app.config.globalProperties.$message = safeMessage;

// 在应用挂载之前，设置全局错误处理
// 屏蔽所有与ResizeObserver相关的错误
const originalConsoleError = console.error;
console.error = function(...args) {
  // 忽略与ResizeObserver或getBoundingClientRect相关的错误
  if (args.length > 0 && 
      (typeof args[0] === 'string' && 
       (args[0].includes('ResizeObserver') || 
        args[0].includes('getBoundingClientRect') ||
        args[0].includes('Element UI') ||
        args[0].includes('Element Plus')))) {
    // 完全静默这些错误
    return;
  }
  
  // 处理Error对象
  if (args.length > 0 && args[0] instanceof Error) {
    const errorMessage = args[0].message || args[0].toString();
    if (errorMessage.includes('ResizeObserver') || 
        errorMessage.includes('getBoundingClientRect') ||
        errorMessage.includes('Element UI') ||
        errorMessage.includes('Element Plus')) {
      // 静默这些错误对象
      return;
    }
  }
  
  // 其他错误正常显示
  return originalConsoleError.apply(this, args);
};

// 设置全局错误处理
window.addEventListener('error', (event) => {
  // 如果错误与ResizeObserver或getBoundingClientRect相关，阻止默认处理
  if (event && event.error && 
      (event.error.message && 
       (event.error.message.includes('ResizeObserver') || 
        event.error.message.includes('getBoundingClientRect')))) {
    // 阻止错误继续传播
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
}, true);

// 处理未捕获的promise rejection
window.addEventListener('unhandledrejection', (event) => {
  // 如果错误与ResizeObserver或getBoundingClientRect相关，阻止默认处理
  if (event && event.reason && 
      (typeof event.reason.message === 'string' && 
       (event.reason.message.includes('ResizeObserver') || 
        event.reason.message.includes('getBoundingClientRect')))) {
    // 阻止rejection继续传播
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
}, true);

// 特别针对webpack-dev-server的overlay错误处理
if (process.env.NODE_ENV === 'development') {
  // 覆盖webpack-dev-server的错误处理
  const originalError = console.error;
  console.error = function(...args) {
    // 检查是否是webpack-dev-server的overlay错误
    if (args.length > 0 && 
        (typeof args[0] === 'string' && 
         args[0].includes('ResizeObserver loop'))) {
      // 忽略这些错误
      return;
    }
    
    // 其他错误正常处理
    return originalError.apply(this, args);
  };

  // 监听DOM变化，移除webpack-dev-server错误overlay
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.addedNodes.length) {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === 1 && node.classList && 
              (node.classList.contains('webpack-dev-server-client-overlay') || 
               node.classList.contains('error-overlay'))) {
            if (node.textContent && node.textContent.includes('ResizeObserver')) {
              node.remove();
            }
          }
        }
      }
    }
  });

  // 开始观察document.body的变化
  observer.observe(document.body, { childList: true, subtree: true });
}

// 挂载应用
app.mount('#app');
