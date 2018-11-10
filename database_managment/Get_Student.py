from database_managment import db_connection
def Get_student():
    connection = db_connection.connect()
    cur = connection.cursor()
    sql_language ='''
    select name,row_id,'pending' from Student_info;
    '''
    #sql = ' describe Student_info; '
    cur.execute(sql_language)
    #cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    connection.commit()
    connection.close( )

    return result

def Check_student():
    connection = db_connection.connect()
    cur = connection.cursor()
    sql_language ='''
    select name from Student_info;
    '''
    #sql = ' describe Student_info; '
    cur.execute(sql_language)
    #cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    connection.commit()
    connection.close( )
    reshaped = []
    for each in result:
        reshaped.append( each[0] )

    return reshaped

def Create_student( student_name ):
    connection = db_connection.connect()
    cur = connection.cursor()
    sql_language ='''
    insert into Student_info (name) values( %s );
    '''
    #sql = ' describe Student_info; '
    cur.execute(sql_language,( student_name ))
    #cur.execute(sql)
    #result = cur.fetchall()
    cur.close()
    connection.commit()
    connection.close( )


def Delete_student( student_name ):
    connection = db_connection.connect()
    cur = connection.cursor()
    sql_language ='''
    delete from  Student_info where name= %s ;
    '''.format( student_name )
    #sql = ' describe Student_info; '
    cur.execute(sql_language,(student_name,))
    #cur.execute(sql)
    #result = cur.fetchall()
    cur.close()
    connection.commit()
    connection.close( )

def Check_date( section,name ):
    sec = section
    stu_name = name
    connection = db_connection.connect()
    cur = connection.cursor()
    sql1 = '''select max(test_date) from  writing_band where student_name='{}';
    '''.format( stu_name )
    sql2 = '''
        select max(test_date) from  speaking_band where student_name='{}';
    '''.format( stu_name )
    sql3 = '''
        select max(test_date) from  correction_rl where type='L' and student_name='{}';
    '''.format( stu_name )
    sql4 = '''
        select max(test_date) from  correction_rl where type='R' and student_name='{}';
    '''.format( stu_name )

    if sec =='writing':
        cur.execute(sql1)
    elif sec =='speaking':
        cur.execute(sql2)
    elif sec =='reading':
        cur.execute(sql4)
    elif sec =='listening':
        cur.execute(sql3)
    result = cur.fetchall()
    connection.close()
    return result

def Visualization( stu,sec,start,end ):
    connection = db_connection.connect()
    cur = connection.cursor()
    sql1 = '''select test_date,total_cal from  writing_band where student_name='{0}' and (test_date between '{1}' and '{2}');
    '''.format( stu,start,end )
    sql2 = '''
        select test_date,total_input from  speaking_band where student_name='{0}' and (test_date between '{1}' and '{2}');
    '''.format( stu,start,end )
    sql3 = '''
        select test_date,band from  correction_rl where type='L' and student_name='{0}' and (test_date between '{1}' and '{2}');
    '''.format( stu,start,end )
    sql4 = '''
        select test_date,band from  correction_rl where type='R' and student_name='{0}' and (test_date between '{1}' and '{2}');
    '''.format( stu,start,end )
    if sec =='writing':
        cur.execute(sql1)
    elif sec =='speaking':
        cur.execute(sql2)
    elif sec =='reading':
        cur.execute(sql4)
    elif sec =='listening':
        cur.execute(sql3)
    result = cur.fetchall()
    connection.close()

    return result