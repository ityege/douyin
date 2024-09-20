import tools
from tqdm import tqdm
import os
import subprocess
import json
import shutil
import sys

conn = tools.connect_db(False)
cur = conn.cursor()
# 删除视频
cur.execute(
    "select id from luzhi.subprocess_status where status='正在录制' and logic_delete  = 0 ")
for film in tqdm(cur.fetchall(), desc='删除中', unit='视频'):
    cur.execute(
        "select film_up,record_film_path,id from luzhi.film_status where id = %s",
        (film[0],))
    film = cur.fetchone()
    film_up = film[0]
    input_file_path = film[1]
    film_id = film[2]
    # 如果文件存在
    if os.path.exists(input_file_path):
        film_time = 0.0
        try:
            # 获取视频长度
            output = subprocess.check_output(
                f"ffprobe -v quiet -print_format json -show_entries format=duration {str(input_file_path)}",
                stderr=subprocess.STDOUT)
            info = json.loads(output.decode('utf-8'))
            film_time = float(info['format']['duration'])
            if film_time < 1800:
                parent_dir = os.path.basename(os.path.dirname(input_file_path))
                file_name = os.path.basename(input_file_path)
                print(f"文件移动,视频长度小于半小时:{film_time}",input_file_path,"->", f"record_tmp_path/{parent_dir}_{file_name}")
                shutil.move(input_file_path, f"record_tmp_path/{parent_dir}_{file_name}")
                print(f"删除视频,视频长度小于半小时{film_time} 视频id:{film_id},视频博主:{film_up},转码路径:{input_file_path}")
                cur.execute(
                    "UPDATE luzhi.subprocess_status SET status = '已经删除', film_length_unix= %s,film_length_string=%s WHERE id = %s",
                    (film_time, tools.format_spend_time_string(film_time), film_id,))
                cur.execute(
                    "UPDATE luzhi.film_status SET film_status = '已经删除' WHERE id = %s", (film_id,))
            else:
                cur.execute(
                    "UPDATE luzhi.subprocess_status SET status = '录制结束', film_length_unix= %s,film_length_string=%s WHERE id = %s",
                    (film_time, tools.format_spend_time_string(film_time), film_id,))
                cur.execute(
                    "UPDATE luzhi.film_status SET film_status = '录制结束' WHERE id = %s", (film_id,))
        #     说明文件损坏,直接删除
        except Exception as e:
            print(e)
            parent_dir = os.path.basename(os.path.dirname(input_file_path))
            file_name = os.path.basename(input_file_path)
            print("文件移动,文件损坏:",input_file_path,"->", f"record_tmp_path/{parent_dir}_{file_name}",file=sys.stderr)
            shutil.move(input_file_path, f"record_tmp_path/{parent_dir}_{file_name}")
            print(f"删除视频,文件损坏,视频id:{film_id},视频博主:{film_up},转码路径:{input_file_path}")
            cur.execute(
                "UPDATE luzhi.subprocess_status SET status = '已经删除', film_length_unix= %s,film_length_string=%s WHERE id = %s",
                (film_time, tools.format_spend_time_string(film_time), film_id,))
            cur.execute(
                "UPDATE luzhi.film_status SET film_status = '已经删除' WHERE id = %s", (film_id,))

    else:
        print(f"文件不存在,视频id:{film_id},视频博主:{film_up},转码路径:{input_file_path}")
        cur.execute(
            "UPDATE luzhi.subprocess_status SET status = '已经删除' WHERE id = %s", (film_id,))
        cur.execute(
            "UPDATE luzhi.film_status SET film_status = '已经删除' WHERE id = %s", (film_id,))

conn.commit()
