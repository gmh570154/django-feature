import pymysql
conn = pymysql.connect(host='172.20.0.2', user='root', passwd="pass4Zentao", db='zentao')
cur = conn.cursor()
cur.execute("SELECT * from zt_user")
for r in cur:
    print(r)
cur.close()
conn.close()