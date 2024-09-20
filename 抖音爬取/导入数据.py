with open("input/input.txt", "r") as f:
    lines = f.readlines()
name = []
url = []
for index, line in enumerate(lines):
    if index % 2 == 0:
        name.append(line.strip())
    else:
        url.append(line.strip())
result_list = []
for i in range(len(name)):
    result_list.append((name[i], url[i]))
import tools

conn = tools.connect_db(False)
cur = conn.cursor()
for result in result_list:
    print(result)
    cur.execute("insert into paqu.paqu_list(film_up,url,logic_delete) values(%s,%s,0)", result)
conn.commit()
