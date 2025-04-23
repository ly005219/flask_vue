



# 1：本地测试

## 1：安装虚拟环境

```
1：首先克隆要测试的代码，到指定文件夹
git clone https://github.com/ly005219/flask_vue.git
2：创建虚拟环境，进入自己要安装的虚拟环境的目录进行创建虚拟环境
cd D:\P_learning\Python3.10_env\test_flask_vue_env (首先你得有这个目录)
切换python的版本，要符合项目的要求版本
py -0 列出安装了的版本号
py -3.10 进入该版本，用exit()来退出，这个3.10为python.exe后面复制之后重新命名的，这样有利于分辨版本号，不然都是python.exe
python --version   在确定好是项目的版本号后进行创建
python -m venv flask_vue_shop_env 创建成功后进入目录找到scripts点进去看到是3.10的版本就OK了也就是对应的版本
3:激活虚拟环境
cd D:\P_learning\Python3.10_env\test_flask_vue_env\flask_vue_shop_env\Scripts
./activate.ps1 这时就进入了这个虚拟环境中


```



## 2：启动项目

### 1：启动后端项目

#### 1:安装所需要的第三方库和依赖

```
1：切换到刚刚创建的虚拟环境，选择对应的解释器
例如在vscode中选择刚刚创建的虚拟环境即可，也就是刚刚创建的虚拟环境的D:\P_learning\Python3.10_env\test_flask_vue_env\flask_vue_shop_env\Scripts\python.exe
2：在VScode打开之后运行，或者在刚刚的cmd运行也可以，安装所需要的第三方库和依赖
pip install -r requirements.txt


```



#### 2：mysql加载sql文件即可

首先声明最开始是使用mysql5.7，后来我使用mysql8版本也是可以的

```
1：建立数据库运行对应的sql文件即可，这里运行flask_shop里面的flask_shop.sql即可
数据库的的字符集是：utf8mb4 排序规则：utf8mb4_unicode_ci

注意注意注意！！！
如果你建立的数据库名字不是flask_shop，那么你需要去对应的config.py文件找到
MYSQL_DB = 'flask_shop' 这行代码改成自己的数据库名字，才能确保项目启动的时候可以正确的链接

如果你使用docker那么你需要把我docker注释的代码给开起来，同样的在redis_cache.py也要开启对应的docker代码


```



#### 3：打开redis服务链接

声明我的版本是3.0.504，其他版本应该也可以兼容因为并没有使用特别新的一些技术

```
1：可以直接来到flask_vue项目下面，直接找到我对应的这个压缩包，压缩然后运行里面的 redis-server.exe即可等待链接


```



#### 4：启动运行

```
直接运行manager.py即可

```



### 2：启动前端项目

前端得下载好node.js版本，我的是v22.11.0，如果你有多个版本可以使用 fnm use 版本号 暂时来切换到项目所需的版本 nvm ls 查看所有版本

```
 1： npm install -g yarn

 2:  yarn install  #安装依赖
 
 3： yarn serve   #启动项目即可
```



## 3：docker部署



```
进入到docker，进入目录运行yml即可
cd flask_vue
docker-compose -f docker-compose.yml -p flask_vue_shop up --build -d


注意
如果你使用docker那么你需要把config的mysql链接docker注释的代码给开起来，同样的在redis_cache.py也要开启对应的docker代码





```

## 4；项目部分效果图

<img width="1280" alt="81998475cbdc697d63c0e52ea63cd83" src="https://github.com/user-attachments/assets/b073f06d-6018-431b-b8db-759cfc64cd31" />

<img width="1280" alt="28155f11d7acc3cca2b8e1fa5d987a6" src="https://github.com/user-attachments/assets/e7108cfa-e0e7-4a76-8542-4d0a0db790ef" />

<img width="1280" alt="f13c3253e0d49ba8b716fb61bb15827" src="https://github.com/user-attachments/assets/9a75aa11-dc6e-4299-9cb2-775eee8c81ab" />

<img width="1280" alt="5610fb6960a4551a5af113b78b528ac" src="https://github.com/user-attachments/assets/43181bff-b1f5-4602-8b1d-9a562fedcd19" />

<img width="1280" alt="8d89f28cc29ef1a22b7b3be5824c760" src="https://github.com/user-attachments/assets/07bd3090-1a2f-4cd7-b367-3b0160b1179f" />








