import pymysql

def connect():
    connection = pymysql.connect(host='ec2db.cmvp0kxmic2d.ap-southeast-2.rds.amazonaws.com', port=3306, user='bahamutedean', passwd='jx13805152868',
                             db='TP',charset='utf8' )
    return connection


if __name__ == '__main__':
    con = connect()
    cur = con.cursor()
    sql = '''
    create table correction_rl ( row_id int auto_increment,
    test_date DATE not null,
    material varchar(20) not null,
    student_name varchar(30) not null,
    type varchar(5) not null,
    band float not null,
    a01 BOOLEAN,
    a02 BOOLEAN,
    a03 BOOLEAN,
    a04 BOOLEAN,
    a05 BOOLEAN,
    a06 BOOLEAN,
    a07 BOOLEAN,
    a08 BOOLEAN,
    a09 BOOLEAN,
    a10 BOOLEAN,
    a11 BOOLEAN,
    a12 BOOLEAN,
    a13 BOOLEAN,
    a14 BOOLEAN,
    a15 BOOLEAN,
    a16 BOOLEAN,
    a17 BOOLEAN,
    a18 BOOLEAN,
    a19 BOOLEAN,
    a20 BOOLEAN,
    a21 BOOLEAN,
    a22 BOOLEAN,
    a23 BOOLEAN,
    a24 BOOLEAN,
    a25 BOOLEAN,
    a26 BOOLEAN,
    a27 BOOLEAN,
    a28 BOOLEAN,
    a29 BOOLEAN,
    a30 BOOLEAN,
    a31 BOOLEAN,
    a32 BOOLEAN,
    a33 BOOLEAN,
    a34 BOOLEAN,
    a35 BOOLEAN,
    a36 BOOLEAN,
    a37 BOOLEAN,
    a38 BOOLEAN,
    a39 BOOLEAN,
    a40 BOOLEAN,
    primary key (row_id) 
     )
    ENGINE=INNODB, CHARSET='utf8mb4';
    '''
    sql1 = '''
    drop table correction_rl;
    '''

    sql2 = '''
    select * from writing_band;
    '''
    cur.execute(  sql )
    #result = cur.fetchall()
    cur.close()
    con.commit(  )
    con.close()
    #print(result)

