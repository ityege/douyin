import csv
import tools
import time
from tqdm import tqdm
import os
from get_all_films import get_all_films
from download_video import download_video

# 获取数据连接,自动提交事务
logger = tools.get_transcode_log_conf('log/download.log')
conn = tools.connect_db(True)
cur = conn.cursor()
cur.execute("select value from paqu.conf where program='kuaishou_paqu' and key='download_path'")
download_path = cur.fetchone()[0]
cur.execute("select value from paqu.conf where program='kuaishou_paqu' and key='cookie'")
cookie = cur.fetchone()[0]

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/myFollow',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'Cookie': cookie,
}
cur.execute("select id,film_up,url  from paqu.paqu_list where logic_delete=0 and platform='kuaishou'")
all_tasks = cur.fetchall()
count = 1
for task in all_tasks:
    print(f"开始下载第{count}个任务,进度:{count}/{len(all_tasks)}")
    logger.info(f"开始下载第{count}个任务,进度:{count}/{len(all_tasks)}")
    id_1 = task[0]
    film_up = task[1]
    userId = task[2]
    download_path_sub = os.path.join(download_path, film_up + "_" + tools.get_current_time0())
    if not os.path.exists(download_path_sub):
        os.makedirs(download_path_sub)
    print(f"开始下载 id: {id_1} film_up:{film_up} userId:{userId}")
    logger.info(f"开始下载 id: {id_1} film_up:{film_up} userId:{userId}")
    start_time = time.time()
    # 获取作者的所有作品
    works = get_all_films(userId, headers)

    # 下载全部视频
    for work in tqdm(works, desc='下载视频中', unit='视频'):
        id1 = work[0]
        title = work[1]
        url = work[2]
        if url:
            download_video(download_path_sub, url, id1, logger)
    # 保存文案为csv文件
    with open(f"{download_path_sub}\\{film_up}_文案.csv", 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(("id", "文案", "url"))
        writer.writerows(works)
    end_time = time.time()
    run_time = end_time - start_time
    cur.execute("delete from paqu.paqu_list where id = %s", (id_1,))
    cur.execute("INSERT INTO paqu.download_over (film_up,url,time_unix,time_string,platform) values (%s,%s,%s,%s,%s)",
                (film_up, userId, tools.get_current_time2(), tools.get_current_time3(), "bilibili"))
    print(
        f"下载结束下载id: {id_1} film_up:{film_up} userId:{userId} 耗费时间:{run_time}->{tools.format_spend_time_string(run_time)}")
    logger.info(
        f"下载结束下载id: {id_1} film_up:{film_up} userId:{userId} 耗费时间:{run_time}->{tools.format_spend_time_string(run_time)}")
    count += 1
conn.close()
