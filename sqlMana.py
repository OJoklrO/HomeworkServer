import pymysql

def Search(sql):
    db = pymysql.connect("182.92.122.205", user="root", passwd="486942", database="zy")

    cursor = db.cursor()

    cursor.execute(sql)

    data = cursor.fetchall()
    db.close()

    return data
