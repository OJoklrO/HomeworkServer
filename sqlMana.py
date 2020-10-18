import pymysql


# 1
def search_id(id):  # 根据课程编号查询课程信息
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    select *
    from course
    where course_id=%s;
    '''
    cur.execute(sql, id)
    ser = cur.fetchall()

    desc = cur.description
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in ser]

    cur.close()
    conn.commit()
    conn.close()
    return data_dict


# 2
def search_name(db):  # 根据课程名称查询课程信息
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    select *
    from course
    where course_name=%s;
    '''
    cur.execute(sql, db)
    ser = cur.fetchall()

    desc = cur.description
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in ser]

    cur.close()
    conn.commit()
    conn.close()
    return data_dict


# 3
def insert_course(id, name, hour, dept, term, sum):  # 课程信息添加
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    insert into course
    value    select capacity,exp_id,exp_name,time,batch,exp_tc,num
    from address natural join experiment natural join exp_time natural join teacher
    where address.room=%s;
    (%s,%s,%s,%s,%s,%s);
    '''
    cur.execute(sql, (id, name, hour, dept, term, sum))
    cur.close()
    conn.commit()
    conn.close()


# 4
def delete_course(id=None, name=None):  # 课程信息删除
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    if id is not None:
        sql = '''
        delete from course where course_id=%s;
        '''
        cur.execute(sql, id)
    elif name is not None:
        sql = '''
        delete from course where course_name=%s;
        '''
        cur.execute(sql, name)
    cur.close()
    conn.commit()
    conn.close()


# 5
def insert_exp(eid, ename, id, caty, hard, hour, cid=None, cname=None):  # 实验列表的增加
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    if cid is not None:
        sql = '''
        insert into experiment
        value
        (%s,%s,%s,%s,%s,%s);
        '''
        cur.execute(sql, (eid, ename, id, caty, hard, hour))
    elif cname != None:
        sql = '''
        insert into experiment
        value
        (%s,%s,%s,%s,%s,%s);
        '''
        cur.execute(sql, (eid, ename, id, caty, hard, hour))
    cur.close()
    conn.commit()
    conn.close()


# 6
def delete_exp(id=None, name=None):  # 实验列表的删除
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    if id is not None:
        sql = '''
        delete from experiment where exp_id=%s
        '''
        cur.execute(sql, id)
    elif name is not None:
        sql = '''
        delete from experiment where exp_name=%s
        '''
        cur.execute(sql, name)
    cur.close()
    conn.commit()
    conn.close()


# 7
def search_room(room):  # 根据实验室查找实验室课程相关信息
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    select capacity,exp_id,exp_name,time,batch,exp_tc,num
    from address natural join experiment natural join exp_time natural join teacher
    where address.room=%s;
    '''
    cur.execute(sql, room)
    ser = cur.fetchall()

    desc = cur.description
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in ser]

    cur.close()
    conn.commit()
    conn.close()
    return data_dict


# 8
def search_stu(na, teac, cla):  # 根据实验，实验员，班级查找学生成绩
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    select stu_id,name,class,grade 
    from student natural join get_grade natural join experiment natural join teacher natural join course_class
    where experiment.exp_name=%s and teacher.exp_tc=%s and student.class=%s; 
    '''
    cur.execute(sql, (na, teac, cla))
    ser = cur.fetchall()

    desc = cur.description
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in ser]

    cur.close()
    conn.commit()
    conn.close()
    return data_dict


# 9
def update_grade(id, name, gr):  # 根据学号，实验名称修改学生成绩
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    update get_grade set grade=%s
    where stu_id=%s and exp_id=(select exp_id
                                from experiment
                                where exp_name=%s
    )
    '''
    cur.execute(sql, (gr, id, name))
    cur.close()
    conn.commit()
    conn.close()


def login(user, passwd):
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = '''
    select *
    from users
    where use_id=%s
    '''
    cur.execute(sql, user)
    ser = cur.fetchall()

    cur.close()
    conn.commit()
    conn.close()

    if len(ser) != 0 and (ser[0][1] == passwd):
        login_suc = True
        return ser[0][2]
    else:
        return 0


def search_table(table_name):
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()
    sql = "select * from " + table_name + ';'

    cur.execute(sql)
    ser = cur.fetchall()

    desc = cur.description
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in ser]

    cur.close()
    conn.commit()
    conn.close()

    return data_dict


def set_ZhC(id, passwd, qx):
    conn = pymysql.connect(host='182.92.122.205', user='root', passwd='486942')
    conn.select_db('zy')
    cur = conn.cursor()

    sql = '''
    select use_id
    from users
    where use_id=%s
    '''
    cur.execute(sql, id)
    ser = cur.fetchall()
    if len(ser) == 0:
        sql1 = '''
        insert into users
        value
        (%s,%s,%s);
        '''
        cur.execute(sql1, (id, passwd, qx))
        cur.close()
        conn.commit()
        conn.close()
        return 1

    else:
        cur.close()
        conn.commit()
        conn.close()
        return 0


if __name__ == '__main__':
    # search_id('15054039')
    # search_name('课程1')
    # insert_course('777', 'name', '10', 'dept', 'term', '10')
    # delete_course(id='777')
    # insert_exp('345', '演示2', '234567', '演示性', '1', '0', '234567', 'None')
    # delete_exp(id='345')
    # search_room('三楼311')
    # update_grade('030501001','实验2-1','100')
    # print(login('rty','111'))
    # print(search_table('course'))
    print(set_ZhC('aaa', '484651', '1'))
