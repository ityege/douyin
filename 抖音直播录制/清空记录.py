import tools

conn = tools.connect_db(True)
cur = conn.cursor()

cur.execute(
    "UPDATE luzhi.short_film SET logic_delete = 1")
cur.execute(
    "UPDATE luzhi.subprocess_status SET logic_delete = 1")
cur.execute(
    "UPDATE luzhi.film_status SET logic_delete = 1")

