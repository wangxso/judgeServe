FROM ubuntu:20.04
RUN apt-get -y update
RUN apt-get -y install python3 python3-pip gcc g++




ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh