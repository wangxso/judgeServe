#基于的基础镜像
FROM python:3

#代码添加到code文件夹
ADD . /usr/src/app

# 设置app文件夹是工作目录
WORKDIR /usr/src/app

# 设置运行环境
RUN mkdir ./dist/
# 安装支持
RUN apt update
RUN apt install -y default-jdk
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

CMD [ "bash", "/usr/src/app/entrypoint.sh" ]
