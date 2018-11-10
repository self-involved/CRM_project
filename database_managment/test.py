from database_managment import Get_Student

Get_Student.Delete_student( '模版' )
#result = Get_Student.Get_student()

'''

from database_managment import db_connection
con = db_connection.connect()
cur = con.cursor()

cur.execute( ''select max(test_date) from  writing_band where student_name= in (陈鑫宇);'' )
result = cur.fetchall()
print(result)

r = Get_Student.Check_date('listening','徐静文')
print(r)

r  = Get_Student.Visualization('叶海博','reading','2018-06-01','2018-10-01')
print(r.__len__())
'''


#from database_managment import db_connection
#con = db_connection.connect()
#cur = con.cursor()
sql = '''
select test_date,total_input from speaking_band where student_name='马婧飏' and test_date>'2018-05-01' and total_input>4.5;
'''
'''
cur.execute(sql)
result = cur.fetchall()
time = []
band =[]
for each in result:
    time.append( each[0] )
    band.append(each[1])
import matplotlib.pyplot as plt
plt.figure( figsize=[5,5] )
plt.scatter( time,band )
plt.savefig( r'/Users/xiaoking/PycharmProjects/CRM_project/static/dashimg/test.jpg' )
plt.show()
'''