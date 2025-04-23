# 使用官方的 Python 3.10 镜像作为基础镜像
FROM python:3.10

# 设置工作目录为 /app
WORKDIR /app

# 创建uploads目录
RUN mkdir -p /app/flask_shop/static/uploads

# 复制requirements.txt文件
COPY Flask_Shop/requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制整个Flask_Shop目录到容器内
COPY Flask_Shop/ .

# 设置环境变量
ENV FLASK_APP=manager.py
ENV PYTHONUNBUFFERED=1

# 暴露 Flask 默认的端口
EXPOSE 5000

# 设置启动命令
CMD ["flask", "run", "--host=0.0.0.0"]

# '''
# 如何使用这个 Dockerfile：
# 构建 Docker 镜像：
# 在项目根目录下运行以下命令：   docker build -t flask_shop .
# 这将创建一个名为 flask_shop 的 Docker 镜像。
# 使用以下命令启动容器：   docker run -p 5000:5000 -d flask_shop
# 这将启动容器，并将本地主机的 5000 端口映射到容器的 5000 端口。
# 访问 http://localhost:5000 即可看到 Flask 应用的欢迎页面。
# '''