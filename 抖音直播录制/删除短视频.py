import shutil

import tools
from tqdm import tqdm
import os
import sys
conn = tools.connect_db(False)
cur = conn.cursor()
# 删除视频
cur.execute(
    "select id from luzhi.short_film where if_delete='删除' and logic_delete  = 0 ")
for film in tqdm(cur.fetchall(), desc='删除中', unit='视频'):
    cur.execute(
        "select film_up,record_film_path,id from luzhi.film_status where id = %s",
        (film[0],))
    film = cur.fetchone()
    film_up = film[0]
    input_file_path = film[1]
    film_id = film[2]
    if os.path.exists(input_file_path):
        parent_dir = os.path.basename(os.path.dirname(input_file_path))
        file_name = os.path.basename(input_file_path)
        print("文件移动:",input_file_path,"->", f"record_tmp_path/{parent_dir}_{file_name}",file=sys.stderr)
        shutil.move(input_file_path, f"record_tmp_path/{parent_dir}_{file_name}")
    else:
        print(f"{input_file_path}文件不存在")
    cur.execute(
        "UPDATE luzhi.short_film SET if_delete = '已经删除' WHERE id = %s", (film_id,))
    cur.execute(
        "UPDATE luzhi.subprocess_status SET status = '已经删除' WHERE id = %s", (film_id,))
    cur.execute(
        "UPDATE luzhi.film_status SET film_status = '视频删除' WHERE id = %s", (film_id,))

conn.commit()
