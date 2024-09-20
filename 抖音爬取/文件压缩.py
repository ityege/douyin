import tools
import os
import shutil

conn = tools.connect_db(True)
cur = conn.cursor()

cur.execute("select value from paqu.conf where program='yasuo' and key='source'")
source = cur.fetchone()[0]
cur.execute("select value from paqu.conf where program='yasuo' and key='dest'")
dest = cur.fetchone()[0]
cur.execute("select value from paqu.conf where program='yasuo' and key='limit'")
limit = cur.fetchone()[0]
limit = int(limit)
for dir in os.listdir(source):
    if limit == 0:
        break
    dir_abs = os.path.join(source, dir)
    dest_7z_path = os.path.join(dest, dir)
    ml = f"7z a -mx0 {dest_7z_path}.7z {dir_abs} >> log\\yasuo.log"
    print(ml, "->", limit)
    status_code = os.system(ml)
    if status_code == 0:
        print("删除目录:", dir_abs)
        shutil.rmtree(dir_abs)
        limit -= 1
    else:
        raise Exception("文件压缩失败,请检查")
