import os
import subprocess
from datetime import datetime

root_path = ""
# 列出root目录下所有目录

dirs = os.listdir(root_path)

for dir in dirs:
    # 拼接目录
    dir_path = os.path.join(root_path, dir)
    # 列出目录下所有文件
    files = os.listdir(dir_path)
    last_time = 0
    last_duration = 0
    last_width = 0
    last_height = 0
    cache_group = []
    cache = []
    files.sort()
    for file in files:
        # 拼接文件路径
        file_path = os.path.join(dir_path, file)
        # 拼接命令
        #         获取文件分辨率和视频长度
        cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 {file_path}"
        result = os.popen(cmd).read()
        width, height, duration = result.split(",")
        filename, ext = os.path.splitext(file)
        # 转换为时间戳（秒级，Unix时间戳）
        timestamp = datetime.strptime(filename, "%Y%m%d%H%M").timestamp()
        # 大于10分钟
        if (timestamp - (last_time + float(last_duration)) > 3600) or last_width != width or last_height != height:
            if len(cache) > 0:
                cache_group.append(cache)
                cache = []
            cache.append(file)
        else:
            cache.append(file)
        last_time = timestamp
        last_duration = duration
        last_width = width
        last_height = height
    cache_group.append(cache)
    for cache in cache_group:
        if len(cache) < 2:
            print(f"{dir}:{cache}:不需要合并")
            continue
        os.chdir(dir_path)
        filelist_content = '\n'.join([f"file '{file}'" for file in cache])
        filelist = open('filelist.txt', 'w')
        filelist.write(filelist_content)
        filelist.close()
        # 使用subprocess和stdin传递文件列表
        output_file_name = f"{int(cache[0].split('.')[0]) - 1}.mp4"
        process = subprocess.Popen(
            f"ffmpeg -f concat -safe 0 -i filelist.txt -c copy -y {output_file_name}",
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(f"{dir}:合并文件:{cache},输出文件:{output_file_name}")

        # 将文件列表内容写入标准输入
        process.stdin.write(filelist_content)
        process.stdin.close()

        # 等待进程完成
        process.wait()
        # 删除合并文件
        for file in cache:
            os.remove(file)
        # 删除filelist文件
        os.remove("filelist.txt")
    # break
