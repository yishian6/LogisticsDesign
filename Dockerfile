FROM python:3.10
WORKDIR /Project/LogisticsDesign

COPY requirements.txt ./
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

ENV LANG C.UTF-8
ENV TZ Asia/Shanghai

