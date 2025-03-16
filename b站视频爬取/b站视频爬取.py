from get_all_videos import get_all_videos
from get_video_cid import get_video_cids
from download_video import download_video
import csv
import tools
import time
from tqdm import tqdm
import os

# 获取数据连接,自动提交事务
logger = tools.get_transcode_log_conf('log/download.log')
conn = tools.connect_db(True)
cur = conn.cursor()
cur.execute("select value from paqu.conf where program='bilibili_paqu' and key='download_path'")
download_path = cur.fetchone()[0]
cur.execute("select value from paqu.conf where program='bilibili_paqu' and key='cookie'")
cookie = cur.fetchone()[0]

headers = {
    'referer': 'https://space.bilibili.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'cookie': cookie,

}
cur.execute("select id,film_up,url  from paqu.paqu_list where logic_delete=0 and platform='bilibili'")
all_tasks = cur.fetchall()
count = 1
for task in all_tasks:
    print(f"开始下载第{count}个任务,进度:{count}/{len(all_tasks)}")
    logger.info(f"开始下载第{count}个任务,进度:{count}/{len(all_tasks)}")
    id_1 = task[0]
    film_up = task[1]
    mid = task[2]
    download_path_sub = os.path.join(download_path, film_up)
    if not os.path.exists(download_path_sub):
        os.makedirs(download_path_sub)
    print(f"开始下载 id: {id_1} film_up:{film_up} mid:{mid}")
    logger.info(f"开始下载 id: {id_1} film_up:{film_up} mid:{mid}")
    start_time = time.time()
    # 获取作者的所有作品
    works = get_all_videos(mid, headers)

    # 获取视频cid
    cid_works = []
    for work in tqdm(works, desc='获取cid中', unit='视频'):
        work = get_video_cids(work, headers, logger)
        cid_works.append(work)
    # 下载全部视频
    for work in tqdm(cid_works, desc='下载视频中', unit='视频'):
        bvid = work[1]
        title = work[2]
        cid = work[3]
        for cid in cid.split(","):
            download_video(download_path_sub, bvid, cid, title, headers, logger)
    # 保存文案为csv文件
    with open(f"{download_path_sub}\\{mid}_{film_up}_文案.csv", 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(("aid", "bvid", "文案", "cid"))
        writer.writerows(cid_works)
    end_time = time.time()
    run_time = end_time - start_time
    cur.execute("delete from paqu.paqu_list where id = %s", (id_1,))
    cur.execute("INSERT INTO paqu.download_over (film_up,url,time_unix,time_string,platform) values (%s,%s,%s,%s,%s)",
                (film_up, mid, tools.get_current_time2(), tools.get_current_time3(), "bilibili"))
    print(
        f"下载结束下载id: {id_1} film_up:{film_up} mid:{mid} 耗费时间:{run_time}->{tools.format_spend_time_string(run_time)}")
    logger.info(
        f"下载结束下载id: {id_1} film_up:{film_up} mid:{mid} 耗费时间:{run_time}->{tools.format_spend_time_string(run_time)}")
    count += 1
conn.close()
