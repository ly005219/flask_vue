import { ElMessage } from 'element-plus';
import { nextTick } from 'vue';

// 全局配置
const config = {
  // 是否开启防抖功能，避免短时间内显示大量相同消息
  enableDebounce: true,
  // 防抖时间，毫秒
  debounceTime: 300,
  // 默认消息持续时间
  duration: 3000
};

// 用于防抖的消息缓存
const messageCache = new Map();

// 检查DOM是否可用
const isDOMAvailable = () => {
  return typeof document !== 'undefined' && document.body !== null;
};

// 防抖函数
const debounce = (fn, delay) => {
  let timer = null;
  return function(...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
      timer = null;
    }, delay);
  };
};

// 构建安全的消息配置
const buildSafeConfig = (options) => {
  if (typeof options === 'string') {
    return {
      message: options,
      appendTo: document.body,
      customClass: 'global-message',
      duration: config.duration,
      onClose: () => {/* 空函数，确保回调安全 */}
    };
  }
  
  return {
    ...options,
    appendTo: document.body,
    customClass: `global-message ${options.customClass || ''}`.trim(),
    duration: options.duration || config.duration,
    onClose: (options.onClose && typeof options.onClose === 'function') 
      ? (...args) => {
          try {
            options.onClose(...args);
          } catch (e) {
            console.debug('消息关闭回调错误，已忽略');
          }
        } 
      : () => {}
  };
};

// 生成消息缓存键
const generateCacheKey = (options) => {
  if (typeof options === 'string') return options;
  return options.message + (options.type || 'info');
};

// 安全显示消息的核心函数
const showMessageSafely = (options) => {
  // 如果DOM不可用，则延迟一次显示
  if (!isDOMAvailable()) {
    return setTimeout(() => safeMessage(options), 100);
  }
  
  try {
    // 配置安全参数
    const safeOptions = buildSafeConfig(options);
    return ElMessage(safeOptions);
  } catch (error) {
    // 在开发环境记录错误但不抛出
    if (process.env.NODE_ENV === 'development') {
      console.debug('消息显示失败，但错误已被处理:', error.message);
    }
    return null;
  }
};

// 防抖包装
const debouncedShowMessage = debounce(showMessageSafely, config.debounceTime);

// 安全包装的消息函数，确保DOM就绪后再显示消息
const safeMessage = (options) => {
  // 如果开启防抖且消息相同，应用防抖逻辑
  if (config.enableDebounce) {
    const cacheKey = generateCacheKey(options);
    if (messageCache.has(cacheKey)) {
      return messageCache.get(cacheKey);
    }
    
    const messageInstance = nextTick(() => debouncedShowMessage(options));
    messageCache.set(cacheKey, messageInstance);
    
    // 从缓存中移除
    setTimeout(() => {
      messageCache.delete(cacheKey);
    }, config.debounceTime + 100);
    
    return messageInstance;
  }
  
  // 不需要防抖，直接显示
  return nextTick(() => showMessageSafely(options));
};

// 创建便捷方法
['success', 'warning', 'error', 'info'].forEach(type => {
  safeMessage[type] = (message, options = {}) => {
    return safeMessage({
      ...options,
      message,
      type
    });
  };
});

// 添加配置方法
safeMessage.config = newConfig => {
  Object.assign(config, newConfig);
  return safeMessage;
};

// 导出安全包装的消息函数
export default safeMessage; 