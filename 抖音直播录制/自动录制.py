import random
import sys
import threading
import tools
import get_url_douyin
import get_url_bilibili
import get_url_kuaishou
import time
import traceback
from datetime import datetime, time as dtime, timedelta
from live_record import live_record

# (id,name,worker_thread,platform)
tasks = []

logger_info, file_handler_info = tools.get_transcode_log_conf("log/record_auto_info.log")
logger_error, file_handler_error = tools.get_transcode_log_conf("log/record_auto_error.log")
is_debug = False


def exception_hook(exctype, value, traceback_local):
    # 写入日志
    logger_error.error("全局异常信息:", exc_info=(exctype, value, traceback_local))


# 设置全局异常处理
sys.excepthook = exception_hook


# 执行任务函数
def run_task(task_info, cur_local):
    global tasks, logger_info, is_debug, logger_error
    if is_debug:
        return "程序处于调试状态,不运行任务"
    id1 = task_info[0]
    name = task_info[1]
    platform = task_info[2]
    # 随机睡眠5到10秒
    time.sleep(random.randint(5, 10))
    # 任务队列里面有这个任务,不需要再获取url
    is_recording = False
    for task in tasks:
        if task[0] == id1:
            is_recording = True
            break

    if not is_recording:
        url = None
        try:
            if platform == "douyin":
                url = get_url_douyin.get_url(id1, name, logger_info, cur_local)
            elif platform == "bilibili":
                url = get_url_bilibili.get_url(id1)
            elif platform == "kuaishou":
                url = get_url_kuaishou.get_url(id1, logger_error, cur_local)
            elif platform == "正能量":
                url = get_url_kuaishou.get_url(id1, logger_error, cur_local)

        except Exception as e:
            # 使用traceback模块获取堆栈跟踪信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 格式化堆栈跟踪信息
            tb_info = ''.join(traceback.format_tb(exc_traceback))
            # 记录错误和堆栈跟踪信息到日志
            logger_error.error("获取url失败: %s\n%s", e, tb_info)

        if url is not None:
            film_time = tools.get_current_time1()
            worker_thread = threading.Thread(target=live_record, args=(
                f"{name}", url, film_time, platform, id1))
            worker_thread.start()
            tasks.append((id1, name, worker_thread, platform))
            cur_local.execute(
                "UPDATE luzhi.auto_record SET last_record_time = %s WHERE id = %s and platform = %s",
                (film_time, id1, platform))
            print(f"任务{id1}:{name}:{platform}已加入调度")
            logger_info.info(f"任务{id1}:{name}:{platform}已加入调度")
            return "任务添加到队列成功"
        else:
            return "获取url为空指针"
    else:
        return "程序处于录制状态,不重复录制"


# 立即拉起函数
def run_now(cur_local):
    global tasks, logger_info
    while True:
        cur_local.execute(
            "select value from luzhi.conf where program = 'douyin_record' and key = 'run_now_is_log'")
        run_now_is_log = cur_local.fetchone()[0]
        cur_local.execute(
            "select id,name,platform from luzhi.auto_record where run_now = 1 ")
        auto_records = cur_local.fetchall()
        if run_now_is_log == '1':
            print(f"{tools.get_current_time3()}:run_now 获取到列表:", len(auto_records), auto_records)
            # logger_info.info(f"run_now 获取到列表:{len(auto_records)},{auto_records}")
        for auto_record in auto_records:
            result = run_task(auto_record, cur_local)
            if run_now_is_log == '1':
                print(f"{tools.get_current_time3()}:run now 启动任务{auto_record}返回结果:{result}")
                # logger_info.info(f"run now 启动任务{auto_record}返回结果:{result}")
            if result == "获取url为空指针":
                print(f"{tools.get_current_time3()}:run_now {auto_record} 获取到url为空,请排查!!!!")
            if result == "程序处于录制状态,不重复录制" or result == "任务添加到队列成功" or result == "获取url为空指针":
                cur_local.execute(
                    "UPDATE luzhi.auto_record SET run_now = 0 WHERE id = %s and platform = %s",
                    (auto_record[0], auto_record[2]))
                if run_now_is_log == '1':
                    print(f"{tools.get_current_time3()}:run now 任务{auto_record} 更新数据库完成")
                    # logger_info.info(f"run now 任务{auto_record} 更新数据库完成")
        if run_now_is_log == '1':
            print(f"{tools.get_current_time3()}:run_now 启动任务{auto_records}结束")
            # logger_info.info(f"run_now 启动任务{auto_records}结束")
        time.sleep(10)


# 核心守护函数
def core_guard(cur_local):
    global tasks, logger_info
    while True:
        cur_local.execute(
            "select value from luzhi.conf where program = 'douyin_record' and key = 'core_guard_is_log'")
        core_guard_is_log = cur_local.fetchone()[0]
        cur_local.execute(
            "select id,name,platform,core_guard_start_time,core_guard_end_time from luzhi.auto_record where "
            "core_guard = 1")
        auto_records = cur_local.fetchall()
        if core_guard_is_log == '1':
            print("core_guard 获取到列表:", len(auto_records), auto_records)
            # logger_info.info(f"core_guard 获取到列表:{len(auto_records)},{auto_records}")
        for auto_record in auto_records:
            # 获取当前时间
            core_guard_start_time = auto_record[3]
            core_guard_end_time = auto_record[4]
            # 将时间字符串转换为time对象
            start_time = dtime(int(core_guard_start_time.split(":")[0]), int(core_guard_start_time.split(":")[1]))
            end_time = dtime(int(core_guard_end_time.split(":")[0]), int(core_guard_end_time.split(":")[1]))
            # 获取当前时间
            current_time = datetime.now().time()
            # 比较当前时间是否在指定范围内
            if start_time <= current_time <= end_time:
                # 函数中会判断是否正在运行
                result = run_task(auto_record, cur_local)
                if core_guard_is_log == '1':
                    print(f"core_guard 启动任务{auto_record}返回结果:{result}")
                    # logger_info.info(f"core_guard 启动任务{auto_record}返回结果:{result}")
            else:
                print(f"core_guard {auto_record}:不在守护时间范围内:{start_time} - {end_time},当前时间:{current_time}")
        if core_guard_is_log == '1':
            print(f"core_guard 启动任务{auto_records}结束")
            # logger_info.info(f"core_guard 启动任务{auto_records}结束")
        time.sleep(60 * 5)


# 这个线程从任务队列中移除任务
def remove_task(cur_local):
    global tasks, logger_info, logger_error
    while True:
        try:
            time.sleep(10)
            for task in tasks:
                id1 = task[0]
                name = task[1]
                worker_thread = task[2]
                platform = task[3]
                if not worker_thread.is_alive():
                    tasks.remove(task)
                    print(f"任务{id1}:{name}:{platform}已完成")
                    logger_info.info(f"任务{id1}:{name}:{platform}已完成")
                    # 失败的任务2分钟后重新拉起来
                    delay = timedelta(minutes=2).total_seconds()
                    threading.Timer(delay, run_task, args=((id1, name, platform), cur_local)).start()
            cur_local.execute(
                "select value from luzhi.conf where program = 'douyin_record' and key='list_task_is_log' ")
            list_task_is_log = cur_local.fetchone()[0]
            if list_task_is_log == "1":
                print(f"{tools.get_current_time3()}:当前调度任务数量:", len(tasks))
                if len(tasks) == 0:
                    continue
                print("运行中任务:", end="")
                for task in tasks:
                    name = task[1]
                    print(f"{name}", end="\t")
                print()
        except Exception as e:
            # 使用traceback模块获取堆栈跟踪信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 格式化堆栈跟踪信息
            tb_info = ''.join(traceback.format_tb(exc_traceback))
            # 记录错误和堆栈跟踪信息到日志
            logger_error.error("remove_task 线程出现问题: %s\n%s", e, tb_info)


# 添加任务
def add_task(cur_local):
    global tasks, logger_info, logger_error

    while True:
        # 获取到所有的url
        try:
            cur_local.execute(
                "select value from luzhi.conf where program = 'record' and key='isstop' ")
            is_stop = cur_local.fetchone()[0]
            if is_stop == '1':
                if len(tasks) == 0:
                    sys.exit(0)
                cur_local.execute(
                    "select value from luzhi.conf where program = 'douyin_record' and key = 'add_task_is_log'")
                add_task_is_log = cur_local.fetchone()[0]
                if add_task_is_log == '1':
                    print("调度处于停止,不新增任务")
                    # logger_info.info("调度处于停止,不新增任务")
            else:
                cur_local.execute(
                    "select id,name,platform from luzhi.auto_record where logic_delete = 0")
                auto_records = cur_local.fetchall()
                start_time = tools.get_current_time2()
                logger_info.info("开始遍历自动录制任务")
                print(f"{tools.get_current_time3()}:开始遍历自动录制任务")
                cur_local.execute(
                    "select value from luzhi.conf where program = 'douyin_record' and key = 'add_task_is_log'")
                add_task_is_log = cur_local.fetchone()[0]
                if add_task_is_log == '1':
                    print(f"{tools.get_current_time3()}:add task start 任务数量:{len(auto_records)} 任务:{auto_records}")
                    # logger_info.info(f"add task start 任务数量:{len(auto_records)} 任务:{auto_records}")
                for auto_record in auto_records:
                    result = run_task(auto_record, cur_local)
                    if add_task_is_log == '1':
                        print(f"{tools.get_current_time3()}:add task 启动任务 {auto_record} 结果{result}")
                        # logger_info.info(f"add task 启动任务 {auto_record} 结果{result}")
                if add_task_is_log == '1':
                    print(f"{tools.get_current_time3()}:add task end 任务数量{len(auto_records)} 任务:{auto_records}")
                    # logger_info.info(f"add task end 任务数量{len(auto_records)} 任务:{auto_records}")
                end_time = tools.get_current_time2()
                print(f"{tools.get_current_time3()}:结束遍历自动录制任务")
                logger_info.info("结束遍历自动录制任务")
                logger_info.info(f"{start_time}--{end_time}--{tools.format_spend_time_string(end_time - start_time)}")
            # 获取当前时间
            now = datetime.now()
            # 获取当前小时
            current_hour = now.hour
            # 判断是否在 18 点到 24 点之间
            if 18 <= current_hour < 24:
                # 这个时间段很多主播开播,随眠1分钟
                time.sleep(60)
            else:
                # 不是这个时间段睡眠10分钟
                time.sleep(600)
        except Exception as e:
            # 使用traceback模块获取堆栈跟踪信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 格式化堆栈跟踪信息
            tb_info = ''.join(traceback.format_tb(exc_traceback))
            # 记录错误和堆栈跟踪信息到日志
            logger_error.error("add_task 线程出现问题: %s\n%s", e, tb_info)


conn0 = tools.connect_db(True)
cur0 = conn0.cursor()
t0 = threading.Thread(target=add_task, args=(cur0,))
t0.start()
conn1 = tools.connect_db(True)
cur1 = conn1.cursor()
t1 = threading.Thread(target=remove_task, args=(cur1,))
t1.start()
conn3 = tools.connect_db(True)
cur3 = conn3.cursor()
t3 = threading.Thread(target=run_now, args=(cur3,))
t3.start()
conn4 = tools.connect_db(True)
cur4 = conn4.cursor()
t4 = threading.Thread(target=core_guard, args=(cur4,))
t4.start()
# 阻塞主线程运行
t0.join()
t1.join()
t3.join()
t4.join()
