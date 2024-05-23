import pymysql
import sys
import os


format = "%Y-%m-%d"
run_env = os.getenv("EVERY_ENV")
if run_env == "dev":
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="lc",
        password="abc12345",
        database="every",
        charset="utf8"
    )
elif run_env == "online":
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="lc",
        password="abc12345",
        database="every",
        charset="utf8"
    )
