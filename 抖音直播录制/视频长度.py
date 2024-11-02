import os
import shutil
import subprocess
import json
import sys

import tools

conn = tools.connect_db(True)
cur = conn.cursor()
# 删除视频
cur.execute(
    "select value from luzhi.conf where program='douyin_record' and key  = 'download_path' ")
download_path = cur.fetchone()[0]
for root, dirs, files in os.walk(download_path):
    for file in files:
        file = os.path.join(root, file)
        execution_time = 0.0
        try:
            output = subprocess.check_output(
                f"ffprobe -v quiet -print_format json -show_entries format=duration {str(file)}",
                stderr=subprocess.STDOUT)
            info = json.loads(output.decode('utf-8'))
            execution_time = float(info['format']['duration'])
            if execution_time < 1800:
                parent_dir = os.path.basename(os.path.dirname(file))
                file_name = os.path.basename(file)
                if "短视频" not in file:
                    print(execution_time / 60, file)
                    print(f"文件短移动,视频长度小于半小时:{execution_time / 60}", file, "->",
                          f"record_tmp_path/{parent_dir}_{file_name}")
                    shutil.move(file, f"record_tmp_path/{parent_dir}_{file_name}")
        except Exception as e:
            print(e)
            print(f"删除视频{file}")
            parent_dir = os.path.basename(os.path.dirname(file))
            file_name = os.path.basename(file)
            print("文件损坏移动:", file, "->", f"record_tmp_path/{parent_dir}_{file_name}", file=sys.stderr)
            shutil.move(file, f"record_tmp_path/{parent_dir}_{file_name}")
