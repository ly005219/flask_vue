/**
 * 高级图像编辑器
 * 支持：
 * - 交互式裁剪
 * - 旋转和缩放
 * - 实时滤镜预览
 * - 压缩质量调整
 */

class AvatarCropper {
  constructor(options = {}) {
    // 默认配置
    this.options = {
      // 容器选择器
      containerSelector: '#avatar-editor',
      // 图片上传输入
      fileInputSelector: '#avatar-input',
      // 图片容器
      imageContainerSelector: '#image-container',
      // 预览容器
      previewSelector: '#preview-container',
      // 裁剪预览
      cropPreviewSelector: '#crop-preview',
      // API路径
      apiEndpoint: '/user/process_avatar/',
      // 上传进度条
      progressSelector: '#upload-progress',
      // 状态消息
      statusSelector: '#status-message',
      // 按钮选择器
      uploadButtonSelector: '#upload-button',
      resetButtonSelector: '#reset-button',
      zoomInSelector: '#zoom-in',
      zoomOutSelector: '#zoom-out',
      rotateLeftSelector: '#rotate-left',
      rotateRightSelector: '#rotate-right',
      // 滑块控制
      qualitySliderSelector: '#quality-slider',
      qualityValueSelector: '#quality-value',
      // 最大文件大小 (5MB)
      maxFileSize: 5 * 1024 * 1024,
      // 裁剪比例 (1:1 圆形头像)
      aspectRatio: 1,
      // 裁剪预览大小
      previewWidth: 200,
      previewHeight: 200,
      // 是否自动应用滤镜
      autoApplyFilter: true,
      // 合并选项
      ...options
    };

    // 状态
    this.state = {
      cropper: null,
      originalFile: null,
      fileType: null,
      filterType: 'none',
      filterIntensity: 0.5,
      quality: 85,
      format: 'JPEG',
      rotation: 0
    };

    // 初始化
    this.init();
  }

  /**
   * 初始化编辑器
   */
  init() {
    // 获取DOM元素
    this.container = document.querySelector(this.options.containerSelector);
    this.fileInput = document.querySelector(this.options.fileInputSelector);
    this.imageContainer = document.querySelector(this.options.imageContainerSelector);
    this.previewContainer = document.querySelector(this.options.previewSelector);
    this.cropPreview = document.querySelector(this.options.cropPreviewSelector);
    this.progressBar = document.querySelector(this.options.progressSelector);
    this.statusMessage = document.querySelector(this.options.statusSelector);
    this.uploadButton = document.querySelector(this.options.uploadButtonSelector);
    this.resetButton = document.querySelector(this.options.resetButtonSelector);
    this.zoomInButton = document.querySelector(this.options.zoomInSelector);
    this.zoomOutButton = document.querySelector(this.options.zoomOutSelector);
    this.rotateLeftButton = document.querySelector(this.options.rotateLeftSelector);
    this.rotateRightButton = document.querySelector(this.options.rotateRightSelector);
    this.qualitySlider = document.querySelector(this.options.qualitySliderSelector);
    this.qualityValue = document.querySelector(this.options.qualityValueSelector);

    // 检查依赖
    if (typeof Cropper === 'undefined') {
      console.error('需要Cropper.js库');
      this.showStatus('缺少Cropper.js库，请加载该库后再试', 'error');
      return;
    }

    // 绑定事件
    this.bindEvents();

    // 禁用上传按钮直到选择图片
    if (this.uploadButton) {
      this.uploadButton.disabled = true;
    }
  }

  /**
   * 绑定事件处理程序
   */
  bindEvents() {
    // 文件选择
    if (this.fileInput) {
      this.fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
          this.loadImage(e.target.files[0]);
        }
      });
    }

    // 按钮事件
    if (this.zoomInButton) {
      this.zoomInButton.addEventListener('click', () => {
        if (this.state.cropper) {
          this.state.cropper.zoom(0.1);
        }
      });
    }

    if (this.zoomOutButton) {
      this.zoomOutButton.addEventListener('click', () => {
        if (this.state.cropper) {
          this.state.cropper.zoom(-0.1);
        }
      });
    }

    if (this.rotateLeftButton) {
      this.rotateLeftButton.addEventListener('click', () => {
        if (this.state.cropper) {
          this.state.cropper.rotate(-90);
          this.state.rotation = (this.state.rotation - 90) % 360;
        }
      });
    }

    if (this.rotateRightButton) {
      this.rotateRightButton.addEventListener('click', () => {
        if (this.state.cropper) {
          this.state.cropper.rotate(90);
          this.state.rotation = (this.state.rotation + 90) % 360;
        }
      });
    }

    // 质量滑块
    if (this.qualitySlider) {
      this.qualitySlider.addEventListener('input', () => {
        this.state.quality = parseInt(this.qualitySlider.value, 10);
        if (this.qualityValue) {
          this.qualityValue.textContent = `${this.state.quality}%`;
        }
      });
    }

    // 滤镜选择
    document.querySelectorAll('input[name="filter"]').forEach(input => {
      input.addEventListener('change', () => {
        if (input.checked) {
          this.state.filterType = input.value === 'none' ? null : input.value;
          
          // 如果自动应用，更新预览
          if (this.options.autoApplyFilter && this.state.cropper) {
            this.updatePreview();
          }
        }
      });
    });

    // 滤镜强度
    const filterIntensitySlider = document.querySelector('#filter-intensity');
    if (filterIntensitySlider) {
      filterIntensitySlider.addEventListener('input', () => {
        this.state.filterIntensity = parseFloat(filterIntensitySlider.value);
        
        // 更新显示的值
        const valueDisplay = document.querySelector('#filter-intensity-value');
        if (valueDisplay) {
          valueDisplay.textContent = `${Math.round(this.state.filterIntensity * 100)}%`;
        }
        
        // 如果自动应用，更新预览
        if (this.options.autoApplyFilter && this.state.cropper) {
          this.updatePreview();
        }
      });
    }

    // 格式选择
    document.querySelectorAll('input[name="format"]').forEach(input => {
      input.addEventListener('change', () => {
        if (input.checked) {
          this.state.format = input.value;
        }
      });
    });

    // 上传按钮
    if (this.uploadButton) {
      this.uploadButton.addEventListener('click', () => {
        this.uploadImage();
      });
    }

    // 重置按钮
    if (this.resetButton) {
      this.resetButton.addEventListener('click', () => {
        this.resetEditor();
      });
    }

    // 拖放上传
    if (this.container) {
      this.container.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.container.classList.add('drag-over');
      });

      this.container.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.container.classList.remove('drag-over');
      });

      this.container.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.container.classList.remove('drag-over');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          this.loadImage(e.dataTransfer.files[0]);
        }
      });
    }
  }

  /**
   * 加载图像到编辑器
   */
  loadImage(file) {
    // 检查文件类型
    if (!file.type.match('image.*')) {
      this.showStatus('请选择有效的图像文件', 'error');
      return;
    }

    // 检查文件大小
    if (file.size > this.options.maxFileSize) {
      this.showStatus(`文件过大，请选择小于 ${this.options.maxFileSize / (1024 * 1024)}MB 的文件`, 'error');
      return;
    }

    // 保存原始文件以供上传
    this.state.originalFile = file;
    this.state.fileType = file.type;

    // 创建图像预览
    const reader = new FileReader();
    reader.onload = (e) => {
      // 清除之前的图像和裁剪器
      if (this.state.cropper) {
        this.state.cropper.destroy();
        this.state.cropper = null;
      }

      // 清除容器
      if (this.imageContainer) {
        this.imageContainer.innerHTML = '';
        
        // 创建新图像元素
        const img = document.createElement('img');
        img.id = 'image-to-crop';
        img.src = e.target.result;
        this.imageContainer.appendChild(img);
        
        // 初始化裁剪器
        this.initCropper(img);
      }
      
      // 显示控件
      document.querySelectorAll('.editor-controls').forEach(el => {
        el.style.display = 'block';
      });
      
      // 启用上传按钮
      if (this.uploadButton) {
        this.uploadButton.disabled = false;
      }
    };
    reader.readAsDataURL(file);
  }

  /**
   * 初始化裁剪器
   */
  initCropper(imageElement) {
    this.state.cropper = new Cropper(imageElement, {
      aspectRatio: this.options.aspectRatio,
      viewMode: 1,
      dragMode: 'move',
      autoCropArea: 0.8,
      restore: false,
      guides: true,
      center: true,
      highlight: false,
      cropBoxMovable: true,
      cropBoxResizable: true,
      toggleDragModeOnDblclick: false,
      ready: () => {
        // 初始化预览
        this.updatePreview();
      },
      crop: () => {
        // 当裁剪框变化时更新预览
        this.updatePreview();
      }
    });
  }

  /**
   * 更新裁剪预览
   */
  updatePreview() {
    if (!this.state.cropper || !this.cropPreview) return;
    
    // 获取裁剪数据
    const cropData = this.state.cropper.getData();
    
    // 构建表单数据
    const formData = new FormData();
    formData.append('image', this.state.originalFile);
    formData.append('crop_data', JSON.stringify({
      x: cropData.x,
      y: cropData.y,
      width: cropData.width,
      height: cropData.height
    }));
    formData.append('rotate', this.state.rotation);
    formData.append('size', this.options.previewWidth);
    formData.append('quality', this.state.quality);
    formData.append('format', this.state.format);
    formData.append('preview', 'true');
    
    // 添加滤镜信息
    if (this.state.filterType) {
      formData.append('filter', this.state.filterType);
      formData.append('filter_intensity', this.state.filterIntensity);
    }
    
    // 显示加载状态
    this.cropPreview.classList.add('loading');
    
    // 发送预览请求
    fetch(this.options.apiEndpoint, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'token': localStorage.getItem('token') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 200) {
        // 更新预览图像
        this.cropPreview.src = data.data.preview;
        this.cropPreview.classList.remove('loading');
        
        // 更新图像信息
        if (data.data) {
          const infoContainer = document.querySelector('#image-info');
          if (infoContainer) {
            infoContainer.innerHTML = `
              <div class="info-item">
                <span class="info-label">原始大小:</span>
                <span class="info-value">${(data.data.original_size / 1024).toFixed(1)} KB</span>
              </div>
              <div class="info-item">
                <span class="info-label">处理后大小:</span>
                <span class="info-value">${(data.data.compressed_size / 1024).toFixed(1)} KB</span>
              </div>
              <div class="info-item">
                <span class="info-label">压缩率:</span>
                <span class="info-value">${data.data.size_reduction}</span>
              </div>
              <div class="info-item">
                <span class="info-label">尺寸:</span>
                <span class="info-value">${data.data.dimensions}</span>
              </div>
              <div class="info-item">
                <span class="info-label">使用质量:</span>
                <span class="info-value">${data.data.quality_used}%</span>
              </div>
            `;
          }
        }
      } else {
        this.showStatus(data.msg || '预览生成失败', 'error');
        this.cropPreview.classList.remove('loading');
      }
    })
    .catch(error => {
      console.error('Preview error:', error);
      this.showStatus('预览生成失败，请重试', 'error');
      this.cropPreview.classList.remove('loading');
    });
  }

  /**
   * 上传处理后的图像
   */
  uploadImage() {
    if (!this.state.cropper || !this.state.originalFile) {
      this.showStatus('请先选择图片', 'error');
      return;
    }
    
    // 禁用上传按钮
    if (this.uploadButton) {
      this.uploadButton.disabled = true;
    }
    
    // 显示进度条
    if (this.progressBar) {
      this.progressBar.style.display = 'block';
      this.progressBar.value = 0;
    }
    
    // 获取裁剪数据
    const cropData = this.state.cropper.getData();
    
    // 构建表单数据
    const formData = new FormData();
    formData.append('image', this.state.originalFile);
    formData.append('crop_data', JSON.stringify({
      x: cropData.x,
      y: cropData.y,
      width: cropData.width,
      height: cropData.height
    }));
    formData.append('rotate', this.state.rotation);
    formData.append('quality', this.state.quality);
    formData.append('format', this.state.format);
    
    // 添加滤镜信息
    if (this.state.filterType) {
      formData.append('filter', this.state.filterType);
      formData.append('filter_intensity', this.state.filterIntensity);
    }
    
    // 创建XHR请求以便跟踪进度
    const xhr = new XMLHttpRequest();
    
    // 进度监听
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentage = Math.round((e.loaded / e.total) * 100);
        if (this.progressBar) {
          this.progressBar.value = percentage;
        }
      }
    });
    
    // 完成监听
    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText);
          if (response.status === 200) {
            this.showStatus(response.msg || '头像上传成功！', 'success');
            
            // 更新页面上所有头像
            this.updateAllAvatars(response.data.avatar);
            
            // 可选：重置编辑器
            // this.resetEditor();
          } else {
            this.showStatus(response.msg || '上传失败', 'error');
          }
        } catch (e) {
          this.showStatus('解析响应失败', 'error');
        }
      } else {
        this.showStatus('上传失败: ' + xhr.statusText, 'error');
      }
      
      // 隐藏进度条，启用上传按钮
      if (this.progressBar) {
        this.progressBar.style.display = 'none';
      }
      if (this.uploadButton) {
        this.uploadButton.disabled = false;
      }
    });
    
    // 错误监听
    xhr.addEventListener('error', () => {
      this.showStatus('网络错误，上传失败', 'error');
      if (this.progressBar) {
        this.progressBar.style.display = 'none';
      }
      if (this.uploadButton) {
        this.uploadButton.disabled = false;
      }
    });
    
    // 发送请求
    xhr.open('POST', this.options.apiEndpoint);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('token', localStorage.getItem('token') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '');
    xhr.send(formData);
  }

  /**
   * 重置编辑器
   */
  resetEditor() {
    // 重置状态
    this.state.originalFile = null;
    this.state.fileType = null;
    this.state.filterType = 'none';
    this.state.filterIntensity = 0.5;
    this.state.quality = 85;
    this.state.format = 'JPEG';
    this.state.rotation = 0;
    
    // 重置文件输入
    if (this.fileInput) {
      this.fileInput.value = '';
    }
    
    // 销毁裁剪器
    if (this.state.cropper) {
      this.state.cropper.destroy();
      this.state.cropper = null;
    }
    
    // 清除图像容器
    if (this.imageContainer) {
      this.imageContainer.innerHTML = '<div class="placeholder">请选择或拖放图片</div>';
    }
    
    // 清除预览图像
    if (this.cropPreview) {
      this.cropPreview.src = '';
    }
    
    // 隐藏控件
    document.querySelectorAll('.editor-controls').forEach(el => {
      el.style.display = 'none';
    });
    
    // 隐藏进度条
    if (this.progressBar) {
      this.progressBar.style.display = 'none';
    }
    
    // 禁用上传按钮
    if (this.uploadButton) {
      this.uploadButton.disabled = true;
    }
    
    // 重置控件值
    if (this.qualitySlider) {
      this.qualitySlider.value = 85;
      if (this.qualityValue) {
        this.qualityValue.textContent = '85%';
      }
    }
    
    // 重置滤镜选择
    document.querySelector('input[name="filter"][value="none"]')?.checked = true;
    
    // 重置滤镜强度
    const filterIntensitySlider = document.querySelector('#filter-intensity');
    if (filterIntensitySlider) {
      filterIntensitySlider.value = 0.5;
      const valueDisplay = document.querySelector('#filter-intensity-value');
      if (valueDisplay) {
        valueDisplay.textContent = '50%';
      }
    }
    
    // 重置格式选择
    document.querySelector('input[name="format"][value="JPEG"]')?.checked = true;
    
    // 清除状态消息
    this.showStatus('', '');
  }

  /**
   * 显示状态消息
   */
  showStatus(message, type = 'info') {
    if (this.statusMessage) {
      this.statusMessage.textContent = message;
      this.statusMessage.className = 'status-message';
      
      if (message) {
        this.statusMessage.classList.add(type);
        this.statusMessage.style.display = 'block';
        
        // 自动隐藏成功消息
        if (type === 'success') {
          setTimeout(() => {
            this.statusMessage.style.display = 'none';
          }, 5000);
        }
      } else {
        this.statusMessage.style.display = 'none';
      }
    }
  }

  /**
   * 更新所有用户头像
   */
  updateAllAvatars(avatarUrl) {
    // 添加时间戳强制刷新
    const url = `${avatarUrl}?t=${new Date().getTime()}`;
    
    // 更新懒加载头像
    document.querySelectorAll('.lazy-avatar').forEach(img => {
      img.setAttribute('data-src', url);
      // 如果图像已加载，直接更新src
      if (img.classList.contains('loaded')) {
        img.src = url;
      }
    });
    
    // 刷新懒加载器
    if (window.avatarLoader && typeof window.avatarLoader.refresh === 'function') {
      window.avatarLoader.refresh();
    }
    
    // 更新普通头像
    document.querySelectorAll('.avatar-img:not(.lazy-avatar)').forEach(img => {
      img.src = url;
    });
  }
}

// 在DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
  // 检查是否有编辑器容器
  const editorContainer = document.querySelector('#avatar-editor');
  if (editorContainer) {
    window.avatarCropper = new AvatarCropper();
  }
}); 