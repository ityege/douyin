# 格式化花费时间
def format_spend_time_string(execution_time):
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    if hours > 0:
        if minutes > 0:
            return f"{hours}小时{minutes}分钟"
        else:
            return f"{hours}小时"
    else:
        return f"{minutes}分钟"


def format_time_string(time1):
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time1))


# 获取数据库连接
def connect_db(autocommit):
    import json
    with open("conf/database.json", "r", encoding="utf-8") as conf:
        database_conf = json.load(conf)
    import psycopg2

    # 数据库连接参数
    conn_params = {
        "dbname": database_conf["postgresql"]["database"],
        "user": database_conf["postgresql"]["username"],
        "password": database_conf["postgresql"]["password"],
        "host": database_conf["postgresql"]["host"],
        "port": database_conf["postgresql"]["port"]
    }
    # 使用connect函数和连接参数创建连接
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = autocommit
    return conn


# 抖音读取配置文件
def douyin_record_read_config(cur):
    cur.execute(
        "select record_url,index from luzhi.record_url where index=(select max(index) from luzhi.record_url)")
    record_url = cur.fetchone()
    url = record_url[0]
    index = record_url[1]
    cur.execute(
        "select film_up from which_one_to_record where is_selected =1 limit 1")
    film_up = cur.fetchone()

    if film_up:
        sub_path = film_up[0]
    else:
        sub_path = ""

    return sub_path, url, index

def get_current_time0():
    import time
    return time.strftime("%Y%m%d", time.localtime())


# 获取当前时间时间格式202408101034
def get_current_time1():
    import time
    return time.strftime("%Y%m%d%H%M", time.localtime())


# 获取当前时间
def get_current_time2():
    import time
    return time.time()


def get_current_time3():
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 获取uuid
def get_uuid():
    import uuid
    return str(uuid.uuid4())


# 获取转码日志配置
def get_transcode_log_conf(log_file):
    import logging
    # 创建日志记录器
    logger = logging.getLogger(log_file)
    # 配置日志文件路径和格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

    # 创建文件处理器并添加到日志记录器
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    # 设置日志级别
    logger.setLevel(logging.INFO)
    return logger
