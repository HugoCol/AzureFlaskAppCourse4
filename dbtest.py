


host =
user =
password =
db =

dblist = []

cursor = conn.cursor()
cursor.execute(f"select * from ")
for i in cursor:
    dblist.append(i)
