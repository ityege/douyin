import tools
import os

# 删除强制停止的视频
result_code = os.system("python 删除强行停止视频.py")
if result_code != 0:
    print("删除强行停止视频失败")
    exit(result_code)
else:
    print("删除强行停止视频成功")

# 删除短视频
conn=tools.connect_db(True)
cursor=conn.cursor()
cursor.execute("update luzhi.short_film set if_delete='删除' where if_delete is null")
result_code = os.system("python 删除短视频.py")
if result_code != 0:
    print("删除短视频失败")
    exit(result_code)
else:
    print("删除短视频成功")

# 删除临时日志
result_code = os.system("python 删除临时日志.py")
if result_code != 0:
    print("删除临时日志失败")
    exit(result_code)
else:
    print("删除临时日志成功")