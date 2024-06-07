# 基于多式联运的零部件与整车智能调度平台后端

## 项目介绍
&emsp;&emsp;本项目基于一汽集团整车与零部件物流发货流程与运作方式，分析统计整车与零部件在现有物流网络与调度的运行成本，采用多目标协同的多式联运思想和基于人工智能对整车与零部件物流网络进行优化，并将现有收集数据、分析结果、研究方法进行整合，设计并搭建面向多式联运的整车与零部件物流网络优化与智能调度平台，逐步推动整个行业物流供需资源的匹配和有效整合，助力一汽公司提高运输效率、降低成本，并确保零部件和整车能够按时准确地送达目的地。

## 项目结构
本项目后端采用了Flask框架，数据库采用MySQL，前端采用Vue框架。

## 开始

### 依赖安装

* `U系Linux`、`Mac`用户可以通过根目录的`install.sh`脚本文件一键安装，如果出现错误也可以同Windows用户一样按照下面的步骤进行安装。
   ```bash
   cd LogisticsDesign
   ./install.sh
   ```

1. 安装MySQL
   进入MySQL或者mariaDB官网下载对应系统的安装包，进行安装即可。Linux用户可以通过命令进行安装

    ```shell script
    sudo apt-get install mysql
    ```

2. 创建数据库

   打开终端，输入如下命令进入MySQL控制台，具体命令根据你自己的MySQL数据库的设置而定

   ```shell script
   sudo mysql -u root -p
   ```

   ```mysql
   create database logistics CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   SHOW DATABASES ;
   ```

   如果控制台输出的内容中包含有`logistics`数据库，则说明数据库创建成功了。

### 初始化

1. 克隆仓库代码

   进行这一步本地机器上必须先配置好git环境。

   ```shell script
   git clone https://github.com/yishian6/LogisticsDesign.git
   ```
2. 首先创建虚拟环境(注意python版本)
   ```shell
   python -m venv venv
   ```

3. 激活虚拟环境(tab自动补全)
   ```shell 
   cd .\venv\Scripts\
   .\activate
   cd ..  
   cd ..
   ```
   在liunx下激活虚拟环境。

   ```shell
   source venv/bin/activate
   ```

4. 安装依赖(确保切换到虚拟环境)
   ```shell
   python -m pip install --upgrade pip  
   pip install -r .\requirements.txt
   ```

5. 按照config_example.ini配置config.ini  
   [mysql]  
   host = 127.0.0.1  
   port = 3306  
   database = logistics  
   username = root  
   passwd = ******


6. 初始化数据库  
   在data目录下添加数据，进入项目的根目录，使用如下命令进行数据库初始化
   ```bash
   cd LogisticsDesign
   # 初始化数据库
   flask create
   ```
   如果希望初始化数据库时不删除表，可以使用alembic建表，在data/current下添加数据，通过db_update函数来初始化数据库
   ```bash
   alembic revision --autogenerate -m "Migration message"
   ```

7. 运行

   ```bash
   flask run
   flask run --host 0.0.0.0 --port 5000
   ```
   打开 http://127.0.0.1:5000 就可以看到页面了。


