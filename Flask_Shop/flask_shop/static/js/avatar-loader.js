/**
 * 用户头像懒加载
 * 在用户滚动到头像所在位置时才加载头像图片
 */

class AvatarLoader {
  constructor(options = {}) {
    // 默认配置
    this.options = {
      selector: 'img.lazy-avatar', // 懒加载头像的选择器
      rootMargin: '0px 0px 50px 0px', // 提前50px加载
      threshold: 0.1, // 当10%的元素可见时加载
      placeholder: '/static/avatar/placeholder.jpg', // 默认占位图
      errorPlaceholder: '/static/avatar/error.jpg', // 加载失败时显示的图片
      ...options
    };

    this.initObserver();
    this.bindEvents();
  }

  /**
   * 初始化IntersectionObserver
   */
  initObserver() {
    // 检查浏览器是否支持IntersectionObserver
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver(this.onIntersection.bind(this), {
        rootMargin: this.options.rootMargin,
        threshold: this.options.threshold
      });

      this.lazyLoadImages();
    } else {
      // 如果不支持，直接加载所有图片
      this.loadAllImages();
    }
  }

  /**
   * 当元素进入视口时的回调
   */
  onIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // 当元素进入视口时，加载图片
        this.loadImage(entry.target);
        // 停止观察这个元素
        this.observer.unobserve(entry.target);
      }
    });
  }

  /**
   * 加载单张图片
   */
  loadImage(imgElement) {
    const src = imgElement.getAttribute('data-src');
    if (!src) return;

    // 创建一个新图片来预加载
    const img = new Image();
    img.onload = () => {
      imgElement.src = src;
      imgElement.classList.add('loaded');
      imgElement.classList.remove('loading');
    };
    img.onerror = () => {
      imgElement.src = this.options.errorPlaceholder;
      imgElement.classList.add('error');
      imgElement.classList.remove('loading');
    };
    
    imgElement.classList.add('loading');
    img.src = src;
  }

  /**
   * 为页面上的所有懒加载图片添加观察器
   */
  lazyLoadImages() {
    const images = document.querySelectorAll(this.options.selector);
    images.forEach(img => {
      // 设置默认占位图
      if (!img.src) {
        img.src = this.options.placeholder;
      }
      // 添加观察器
      this.observer.observe(img);
    });
  }

  /**
   * 直接加载所有图片（不支持IntersectionObserver的回退方案）
   */
  loadAllImages() {
    const images = document.querySelectorAll(this.options.selector);
    images.forEach(img => {
      this.loadImage(img);
    });
  }

  /**
   * 绑定事件监听器，如页面内容变化时重新检查懒加载图片
   */
  bindEvents() {
    // 页面内容变化时（如AJAX加载新内容）重新检查
    const mutationCallback = (mutationsList) => {
      for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
          this.lazyLoadImages();
        }
      }
    };

    // 创建一个MutationObserver实例
    if ('MutationObserver' in window) {
      const observer = new MutationObserver(mutationCallback);
      observer.observe(document.body, { childList: true, subtree: true });
    }

    // 窗口大小改变时重新检查
    window.addEventListener('resize', this.lazyLoadImages.bind(this));
  }

  /**
   * 手动刷新，检查新添加的图片
   */
  refresh() {
    this.lazyLoadImages();
  }
}

// 创建默认实例并在DOM加载后初始化
document.addEventListener('DOMContentLoaded', () => {
  window.avatarLoader = new AvatarLoader();
}); 