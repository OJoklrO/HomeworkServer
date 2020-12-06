import pymysql
import random


def insert():
    print("insert start")

    users = []
    for num in range(1, 1000000):
        users.append((str(num), 'Downtown', random.randint(100, 500)))

    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='1234', port=3307)
    conn.select_db('BANK026')
    cur = conn.cursor()
    sql = '''insert into ACCOUNT026
    value
    (%s, %s, %s);
    '''
    cur.executemany(sql, users)

    conn.commit()
    cur.close()
    conn.close()

    print("insert end")


if __name__ == '__main__':
    insert()
