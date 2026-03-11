import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Afd657216",
    database="student_score"
)

print("连接成功")