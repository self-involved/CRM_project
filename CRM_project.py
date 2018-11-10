from flask import Flask,render_template,send_from_directory,Markup,url_for,request,jsonify
from markdown import markdown,markdownFromFile
from bs4 import BeautifulSoup as bs
#sys.path.insert(0,' /Users/xiaoking/PycharmProjects/CRM_project ')

app = Flask(__name__)

hello_index = '/Users/xiaoking/PycharmProjects/CRM_project/templates/TriangularPlus.html'
student_index = '/Users/xiaoking/PycharmProjects/CRM_project/templates/Student.html'

dashboard_index = '/Users/xiaoking/PycharmProjects/CRM_project/templates/Dashboard.html'

@app.route('/')
def index():
    with open( hello_index,'r',encoding='utf-8' ) as f:
        xml = f.read()
    xml = Markup( xml )
    return xml


@app.route('/Student',methods=['POST', 'GET'])
def Student():
    '''
    with open( student_index,'r',encoding='utf-8' ) as f:
        xml = f.read()
    xml = Markup( xml )
    '''
    '''
    from database_managment import Get_Student
    student_list = Get_Student.Check_student()
    import time
    time.sleep(1)

    if request.method == 'POST':
        stu_name = request.form['name']

        if stu_name in student_list:
            message = stu_name+' exists in the data warehouse! '

        else:
            try:
                Get_Student.Create_student(stu_name)
                message = stu_name + ' saved in the data warehouse! '
            except:
                message = ' Error occurs, contact administrator '
            #return render_template('complete.html', stu_name=stu_name)
    '''

    return render_template('Student.html')

@app.route('/Student/student_name')
def Student_info(  ):

    from database_managment import Get_Student
    result = Get_Student.Get_student()
    import time
    time.sleep(1)

    return render_template( 'student_info.html',result = result )

#print(url_for(Student))

@app.route('/Student/register',methods=['POST', 'GET'])
def Student_create(  ):
    from database_managment import Get_Student
    student_list = Get_Student.Check_student()
    import time
    time.sleep(1)

    if request.method == 'GET':
        stu_name = request.args.get( 'name','' )



        if stu_name in student_list:
            return render_template( 'alert.html',student_name = stu_name )

        else:
            try:
                Get_Student.Create_student(stu_name )
            except:
                stu_name = 'Error'
            return render_template('complete.html',stu_name = stu_name)


@app.route('/Band')
def Band():
    from database_managment import Get_Student
    student_list = Get_Student.Check_student()
    import numpy as np
    Band = np.linspace(0.0,9.0,19,endpoint=True)
    Band=np.delete(Band,12)
    import datetime
    today = str(datetime.date.today())
    Writing_Band = [ 'TR(W)','CC(W)','LR(W)','GRA(W)','Total(W)' ]
    Speaking_Band = [ 'FC(S)','LR(S)','GRA(S)','PR(S)','Total(S)' ]
    number = list( range(1,41) )
    return render_template('Band.html',content = student_list,Band=Band,Writing_Band=Writing_Band,Speaking_Band=Speaking_Band,today=today,number=number)

@app.route('/Band/query',methods=['POST','GET'])
def Query(  ):
    if request.method=='GET':
        from database_managment import Get_Student
        section = request.args.get('Section','')
        stu_name = request.args.get('Name(Query)','')
        try:
            result = Get_Student.Check_date(section,stu_name)[0][0]
            return 'the latest update time of '+stu_name+' is :' + result.strftime( '%Y-%m-%d' )
        except:
            return  'there is no record for '+stu_name

    else:
        return '1'

@app.route('/Band/feedback',methods=['POST','GET'])
def Feedback():
    if request.method=='GET':
        date_W = request.args.get('user_date(Writing)','')
        name_W = request.args.get('Name(Writing)','')
        task = request.args.get('Task','')
        TR_W = request.args.get('TR(W)','')
        CC_W = request.args.get('CC(W)','')
        LR_W = request.args.get('LR(W)','')
        GRA_W = request.args.get('GRA(W)','')
        Total_W = request.args.get('Total(W)','')
        date_S = request.args.get('user_date(Speaking)','')
        name_S = request.args.get('Name(Speaking)','')
        FC_S = request.args.get('FC(S)','')
        LR_S = request.args.get('LR(S)','')
        GRA_S = request.args.get('GRA(S)','')
        PR_S = request.args.get('PR(S)','')
        Total_S = request.args.get('Total(S)','')
        date_R = request.args.get('user_date(Reading)', '')
        name_R = request.args.get('Name(Reading)', '')
        date_L = request.args.get('user_date(Listening)', '')
        name_L = request.args.get('Name(Listening)', '')
        Listening = request.args.getlist('Listening_number')
        Reading = request.args.getlist('Reading_number')
        '''
        return 'Writing:'+date_W + name_W + task + ':' + TR_W +','+CC_W+','+LR_W+','+GRA_W+','+Total_W+'\n'+\
               'Speaking:'+date_S + name_S  + ':' + FC_S +','+LR_S+','+GRA_S+','+PR_S+','+Total_S+'\n'+\
               'Reading'+date_R + name_R + jsonify(customers=Reading) +'\n'+\
               'Listening' +date_L + name_L + jsonify(customers=Listening)
        '''
        print(Reading)
        return jsonify(customers=Reading)
    else:
        return '1'



@app.route('/Dashboard')
def Dashboard( ):
    from database_managment import Get_Student
    student_list = Get_Student.Check_student()
    import datetime
    today = str(datetime.date.today())
    yesterday = str( datetime.date.today()+datetime.timedelta(days=-1) )
    return render_template( 'Dashboard.html',content=student_list,today = today,yesterday=yesterday )

@app.route('/Dashboard/visualization',methods=['POST','GET'])
def visualization():
    if request.method=='GET':
        name = request.args.get('Name(Dash)','')
        start = request.args.get('start_date','')
        end = request.args.get('end_date','')
        sec = request.args.get('Dash_Section','')
        from database_managment import Get_Student
        result = Get_Student.Visualization(name,sec,start,end)
        if len(result) > 1:
            period=[]
            band =[]
            for each in result:
                period.append( each[0])
                band.append(each[1])
            title = name+'_'+sec
            import matplotlib.pyplot as plt
            from matplotlib.font_manager import FontProperties

            plt.style.use('ggplot')
            font = FontProperties(fname=r'/System/Library/Fonts/STHeiti Light.ttc', size=14)
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure( figsize=[12,6] )
            plt.subplot( 121 )
            plt.plot( period,band,'b--' )

            plt.xticks( rotation=45 )
            #plt.legend()
            plt.subplot(122)
            import seaborn as sns
            sns.distplot( band )

            path = '/Users/xiaoking/PycharmProjects/CRM_project/static/dashimg/'+title+'.jpg'
            link = '/static/dashimg/'+title+'.jpg'
            plt.title(title, fontproperties=font, fontsize='small')
            plt.savefig( path )
            import numpy as np
            avg = round(np.mean( band ),2)
            att = band.__len__()
            content = [ name,avg,att ]
            return render_template('visualization.html',link=link,title=title,content=content)

        else:
            return name+' has no records during the input period, pls check again\n '
    else:
        return 'ERROR'


if __name__ == '__main__':
    app.run('0.0.0.0',port=8900,threaded=True)
