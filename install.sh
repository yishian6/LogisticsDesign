#!/bin/bash

# 创建mysql数据库
read -p "请输入数据库主机名:" hostname
read -p "请输入数据库端口号:" port
read -p "请输入数据库连接用户名:" db_username
read -p "请输入数据库连接密码:" db_password
db_name='zywj'

LOGIN_CMD="mysql -h${hostname} -P${port} -u${db_username} -p${db_password}"


echo ${LOGIN_CMD}

# 创建数据库
create_database() {
    echo "create database ${db_name}"

    create_db_sql="CREATE DATABASE IF NOT EXISTS ${db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
    echo ${create_db_sql} | ${LOGIN_CMD}

    if [ $? -ne 0 ]
    then
        echo "create database ${db_name} failed..."
        exit 1
    else
        echo "succeed to create database ${db_name}"
    fi
}

create_database

python3 -m venv venv
source venv/bin/activate
pip install --default-timeout=1000 --no-cache-dir -r requirements.txt
flask create
flask run
