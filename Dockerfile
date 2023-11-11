# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 将当前目录内容复制到容器的 /app 中
ADD . /app

# 安装在 requirements.txt 中列出的任何需要的包
RUN pip install --no-cache-dir -r requirements.txt

# 使端口8000可供此应用使用
EXPOSE 8000

# 运行 main.py 时，容器将运行以下命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]