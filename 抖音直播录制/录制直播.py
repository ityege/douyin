import subprocess
import os
import tools
import time
import sys
import json

conn = tools.connect_db(True)
cur = conn.cursor()
cur.execute("select value from luzhi.conf where program='douyin_record' and key='download_path'")
download_path = cur.fetchone()[0]
cur.execute("select value from luzhi.conf where program='znl' and key='download_path'")
download_path_znl = cur.fetchone()[0]
sub_path = sys.argv[1]
url = sys.argv[2]
film_time = sys.argv[3]
index = sys.argv[4]
platform = sys.argv[5]
short_id = sys.argv[6]
logger = tools.get_transcode_log_conf(f"./record_tmp_path/{film_time}_{sub_path}_自动录制_{platform}.log")


def exception_hook(exctype, value, traceback):
    # 写入日志
    logger.error("异常信息:", exc_info=(exctype, value, traceback))


# 设置全局异常处理
sys.excepthook = exception_hook
if platform == '正能量':
    download_path = download_path_znl
film_id = tools.get_uuid()
# 如果子目录不存在，就创建子目录
if not os.path.exists(os.path.join(download_path, sub_path)):
    os.makedirs(os.path.join(download_path, sub_path))
# 输出文件路径
output_file_path = os.path.join(download_path, sub_path, film_time) + ".mp4"
# 命令
# b站直接要伪装浏览器,直接ffmpeg会被拒绝
if platform == 'bilibili':
    command = f'wget --header="Accept:application/json, text/plain, */*" --header="Accept-Encoding:gzip, deflate, br" --header="Accept-Language:zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2" --header="Origin:https://live.bilibili.com" --header="Referer:https://live.bilibili.com/{short_id}" --header="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0" "{url}" -O "{output_file_path}"'
else:
    command = f"ffmpeg -i  \"{url}\" -c copy -y \"{output_file_path}\""
start_time = tools.get_current_time2()
log = open(f"./record_tmp_path/{film_time}_{sub_path}.log", "w")
process = subprocess.Popen(command,
                           stdout=log,
                           stderr=subprocess.STDOUT,
                           text=True)
cur.execute(f'''
INSERT INTO luzhi.film_status (
    id,
    film_up,
    film_status,
    record_command,
    record_film_path,
    record_process_id,
    record_time_start_unix,
    record_time_start_string,
    logic_delete
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
''', (film_id, sub_path, '正在录制', command, output_file_path, process.pid, start_time,
      tools.format_time_string(start_time), 0))
cur.execute("INSERT INTO luzhi.subprocess_status (id,status,film_up,index,logic_delete) values (%s,%s,%s,%s,%s)",
            (film_id, '正在录制', sub_path, index, 0))

# 记录日志
logger.info(
    f"视频录制开始：{sub_path},视频id：{film_id},录制命令：{command},进程id:{process.pid},输出目录：{output_file_path},进程id：{process.pid}，开始录制时间：{tools.format_time_string(start_time)}")
# 等待子进程结束
# 增加强行停止的逻辑
is_stop = False
while process.poll() is None:
    time.sleep(10)
    cur.execute("SELECT status from luzhi.subprocess_status  where id= %s", (film_id,))
    if cur.fetchone()[0] == 'stop' and is_stop is False:
        process.kill()
        logger.info("直播录制被强制停止,由于进程必须强制停止才可以停止,输出文件损坏.")
        is_stop = True
# 等待进程释放文件占用
end_time = tools.get_current_time2()
# 计算执行时
execution_time = end_time - start_time
try:
    output = subprocess.check_output(
        f"ffprobe -v quiet -print_format json -show_entries format=duration {output_file_path}",
        stderr=subprocess.STDOUT)
    info = json.loads(output.decode('utf-8'))
    film_time = float(info['format']['duration'])
except Exception as e:
    logger.error("执行时间获取失败,文件长度设置为0")
    logger.error(e)
    film_time = 0.0
# 格式化执行时间
formatted_execute_time = tools.format_spend_time_string(execution_time)
formatted_film_time = tools.format_spend_time_string(film_time)
cur.execute(f'''
UPDATE luzhi.film_status
SET
    film_status = '录制结束',
    record_time_end_unix = %s,
    record_time_end_string = %s,
    record_spend_time_unix = %s,
    record_spend_time_string = %s
WHERE
    id = %s
''', (end_time, tools.format_time_string(end_time), execution_time, formatted_execute_time, film_id))
if film_time < 1800:
    cur.execute(f'''
    INSERT INTO luzhi.short_film (
        id,
        film_up,
        path,
        film_length_unix,
        film_length_string,
        logic_delete
    )
    VALUES (%s,%s,%s,%s,%s,%s);
    ''', (film_id, sub_path, output_file_path, film_time,
          formatted_film_time, 0))
cur.execute("UPDATE luzhi.subprocess_status SET status=%s ,film_length_unix=%s,film_length_string=%s where id= %s",
            ('录制结束', film_time, formatted_film_time, film_id))

logger.info(
    f"视频录制结束：{sub_path},输出目录：{output_file_path},开始录制时间：{tools.format_time_string(start_time)}，结束录制时间：{tools.format_time_string(end_time)}，录制时长：{formatted_execute_time}")
# 输出到控制台
logger.info(f"视频长度为: {formatted_film_time}")
with open("log/record_over.txt", "a") as f:
    f.write(f"{tools.get_current_time3()}->{film_id}->{film_time}->{sub_path}->{formatted_film_time}\n")

conn.close()
