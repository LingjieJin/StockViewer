# Dockerfile

# 1. 使用一个轻量级的 Python 官方镜像作为基础
FROM python:3.9-slim

# 2. 在容器内创建一个工作目录
WORKDIR /app

# 3. 复制依赖文件到工作目录
COPY requirements.txt .

# 4. 安装依赖
#    使用国内镜像源加速下载
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 复制项目所有文件到工作目录
COPY . .

# 6. 声明容器将要监听的端口
EXPOSE 8000

# 7. 定义容器启动时执行的命令
#    使用 Gunicorn 启动应用
#    -w 4: 启动4个工作进程
#    -b 0.0.0.0:8000: 绑定到所有网络接口的8000端口
#    app:app: 指定运行 app.py 文件中的 app 实例
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]