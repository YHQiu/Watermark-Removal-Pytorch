# 使用带有CUDA 11.1支持的Ubuntu 20.04镜像作为基础镜像
FROM pytorch/pytorch:1.11.0-cuda11.8-cudnn8-runtime

# 安装您的应用程序需要的其他依赖项
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# 将您的应用程序代码复制到容器内
COPY . /app
WORKDIR /app

# 指定容器启动时执行的命令
CMD ["sh", "startup.sh"]
