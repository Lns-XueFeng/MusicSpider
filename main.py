import sqlite3


def insert_data(data):
    conn = sqlite3.connect("Newkuwo_SongUrls.db")
    cusor = conn.cursor()
    sql = "insert into songUrls(name, songName, songUrl) values(?, ?, ?)"
    cusor.execute(sql, data)
    conn.commit()
    cusor.close()
    conn.close()


def check_data():
    # 连接数据库(如果不存在则创建)
    conn = sqlite3.connect('kuwo_SongUrls.db')

    # 创建游标
    cursor = conn.cursor()

    # 查询数据 e1 sql语句:select * from 表名 where 列名=?
    sql = "select * from songUrls"
    values = cursor.execute(sql)
    count = 1
    for i in values:
        data = (i[1],i[2],i[3])
        try:
            insert_data(data)
            print(" 成功插入数据{}条".format(count))
            count = count + 1
        except:
            print("跳过重复数据插入失败以达到新数据库不重复")

    # 提交事物
    conn.commit()  # 查询数据可以不写这一行代码不需要提交数据

    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()

check_data()