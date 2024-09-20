import time

import tools
import douyin_download

logger = tools.get_transcode_log_conf('log/download.log')
conn = tools.connect_db(True)
cur = conn.cursor()
cur.execute("select value from paqu.conf where program='douyin_paqu' and key='download_path'")
download_path = cur.fetchone()[0]
cur.execute("select id,film_up,url from paqu.paqu_list where logic_delete=0 ")
all_tasks = cur.fetchall()
if len(all_tasks) == 0:
    print("没有需要下载的任务")
    exit(0)
count = 1
for film_up in all_tasks:
    print(f"开始下载第{count}个任务,进度:{count}/{len(all_tasks)}")
    id_1 = film_up[0]
    film_up_name = film_up[1]
    url = film_up[2]
    user_id = url.split('/')[-1]
    print(f"开始下载 id: {id_1} film_up:{film_up_name} url:{url}")
    logger.info(f"开始下载 id: {id_1} film_up:{film_up_name} url:{url}")
    start_time = time.time()
    #  开始下载
    douyin_download.download_video(url, download_path, user_id, logger, cur, conn, id_1, film_up_name)
    #  下载完成
    cur.execute("delete from paqu.paqu_list where id = %s", (id_1,))
    cur.execute("INSERT INTO paqu.download_over (film_up,url,time_unix,time_string) values (%s,%s,%s,%s)",
                (film_up_name, url, tools.get_current_time2(), tools.get_current_time3()))
    # 提交事务
    end_time = time.time()
    run_time = end_time - start_time
    print(
        f"下载结束下载id: {id_1} film_up:{film_up_name} url:{url} 耗费时间:{run_time}->{tools.format_spend_time_string(run_time)}")
    logger.info(
        f"下载结束下载id: {id_1} film_up:{film_up_name} url:{url} 耗费时间:{run_time}->{tools.format_spend_time_string(run_time)}")
    count += 1
conn.close()
