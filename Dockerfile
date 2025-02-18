# 使用官方的 Python 3.10 镜像作为基础镜像
FROM python:3.10

# 设置工作目录为 当前路径下的Flask_Shop
WORKDIR /app


# 将当前目录的内容复制到工作目录中
COPY Flask_Shop /app

# 创建虚拟环境
RUN python -m venv /opt/venv

# 激活虚拟环境并安装项目的依赖
RUN /opt/venv/bin/pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 设置环境变量，使用虚拟环境中的 Python 和 pip
ENV PATH="/opt/venv/bin:$PATH"

# 暴露 Flask 默认的端口
EXPOSE 5000

# 设置环境变量，告诉 Flask 使用哪个应用
ENV FLASK_APP=manager.py

# 运行 Flask 应用
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