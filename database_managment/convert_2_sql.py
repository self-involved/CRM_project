#from database_managment import db_connection
import pandas as pd
import numpy as np
import xlrd

def convert_adverse_data(list_value):
    new_list_1 = []
    final_list = []
    for blank in map(lambda x: np.nan if x == '练习'  else x, list_value):
        new_list_1.append(blank)
    for each in new_list_1:
        value=str(each).split('-')[0]
        value=str(value).split('+')[0]
        value = float(value.replace('阶测','').replace('左右',''))
        #value = str(value )
        final_list.append(float(value))
    return final_list


def Output_Judge( a, b, c, d ):
    sum = a+b+c+d
    if sum>=16:
        if ( sum/4 ) % 1 == 0.25 or ( sum/4 ) % 1 == 0.75 :
            return sum / 4 + 0.25
        elif ( sum/4 ) % 1 == 0.625 or ( sum/4 ) % 1 == 0.375:
            return sum // 4 + 0.5
        elif ( sum/4 ) % 1 == 0.125:
            return sum // 4
        elif ( sum/4 ) % 1 == 0.875:
            return sum // 4 + 1
        else:
            return sum / 4

def academic_result( grade ):
    if grade>38:
        return 9.0
    elif grade>36:
        return 8.5
    elif grade>34:
        return 8.0
    elif grade>32:
        return 7.5
    elif grade>29:
        return 7.0
    elif grade>26:
        return 6.5
    elif grade>22:
        return 6.0
    elif grade>19:
        return 5.5
    elif grade>15:
        return 5.0
    elif grade>12:
        return 4.5
    elif grade>9:
        return 4.0
    elif grade>5:
        return 3.5
    elif grade>3:
        return 3.0
    elif grade==3:
        return 2.5
    elif grade==2:
        return 2.0
    else:
        return 1.0

writing_path = r'/Users/xiaoking/Downloads/tp/分数统计 写作10.6.xlsx'

def convert_writing( path = writing_path ):
    name_list = xlrd.open_workbook( path ).sheet_names()
    name_list.remove( '模板' )

    content=pd.DataFrame(  )

    for each in name_list:
        content_temp = pd.read_excel( writing_path,sheet_name=each )
        content_temp['日期']=content_temp['日期'].fillna( method='pad' )
        content_temp.dropna( inplace=True )
        content_temp['姓名']=each
        content = content_temp.append( content )

    content['TA'] = convert_adverse_data(content['TA'].values)
    content['CC'] = convert_adverse_data(content['CC'].values)
    content['LR'] = convert_adverse_data(content['LR'].values)
    content['GRA'] = convert_adverse_data(content['GRA'].values)
    content['总分'] = convert_adverse_data(content['总分'].values)
    content.columns = [ 'test_date','task','type','ta','cc','lr','gra','total_input','student_name' ]
    total = []

    for i in range(len(content)):
            #print(writing_final.iat[i,0])
            score = Output_Judge(float(content.iat[i, 3]), float(content.iat[i, 4]), float(content.iat[i, 5]),
                                           float(content.iat[i, 6]))
            total.append(score)


    content['total_cal'] = total
    content.reset_index(drop=True,inplace=True)
    return content

def sql_writing(  ):
    content = convert_writing()
    from database_managment import db_connection
    con = db_connection.connect()
    #content.to_sql( 'writing_band_test',con,if_exists='replace',index=False )



    #content['task']=content['task'].astype(str)
    #content['type']=content['type'].astype(str)

    #content['student_name']=content['student_name'].astype(str)

    #print( content.dtypes )
    value = content.values
    sql = '''
    insert into writing_band ( test_date,task,type,ta,cc,lr,gra,total_input,student_name,total_cal ) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s );
    '''
    cur = con.cursor()
    for each in value:
        cur.execute( sql,( str(each[0]),str(each[1]),str(each[2]),str(each[3]),str(each[4]),str(each[5]),str(each[6]),str(each[7]),str(each[8]),str(each[9]) ) )

    cur.close()
    con.commit()
    con.close()

speaking_path = r'/Users/xiaoking/Downloads/tp/分数统计 口语10.5.xlsx'
def convert_speaking(path = speaking_path):
    name_list = xlrd.open_workbook(path).sheet_names()
    #name_list.remove('模板')
    #print( name_list )
    temp = pd.DataFrame()
    for each in name_list:
        content = pd.read_excel( path,sheet_name=each )
        #print( content )
        #print( content.index )
        #print(content.columns )
        #print( content.loc['日期'].values.tolist() )
        try:
            content.columns = content.loc['日期'].values.tolist()
        except:
            print( each )
        content.drop( index = '日期',inplace=True )
        content['总分']=content['总分'].apply(str)
        #print( content.dtypes )
        #print(content['总分'].str.contains('练习'))
        content['总分'].where(~content['总分'].str.contains('练习'),'4.0',inplace=True)
        content['姓名'] = each
        temp = content.append( temp )
    temp.dropna( axis=1,how='all',inplace=True )
    temp['part1话题'].fillna('UNKONWN',inplace=True)
    temp['part2话题'].fillna('UNKONWN',inplace=True)
    temp.fillna('0.0',inplace=True)
    total = convert_adverse_data( temp['总分'] )
    temp['总分']=total
    temp['日期'] = temp.index
    return temp

def sql_spraking(  ):
    content = convert_speaking()
    from database_managment import db_connection
    con = db_connection.connect()

    value = content.values
    sql = '''
            insert into speaking_band ( test_date,part1,part2,fc,gra,lr,pro,total_input,student_name ) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s );
            '''

    cur = con.cursor()
    for each in value:
        cur.execute(sql, (
            str(each[8]), str(each[4]), str(each[5]), str(each[0]), str(each[1]), str(each[2]), str(each[3]),
            str(each[6]),
            str(each[7])))

    cur.close()
    con.commit()
    con.close()

def convertion_R_L(  ):
    listening_path = r'/Users/xiaoking/Downloads/tp/错题整理 听力10.7.xlsx'

    name_list = xlrd.open_workbook(listening_path).sheet_names()
    temp = pd.DataFrame()
    for each in name_list:
        content = pd.read_excel( listening_path,sheet_name=each )
        content['姓名']=each
        content.dropna(how='any',inplace=True)
        temp = content.append(temp)
    readinging_path = r'/Users/xiaoking/Downloads/tp/错题整理 阅读10.7.xlsx'
    name_list = xlrd.open_workbook(readinging_path).sheet_names()
    for each in name_list:
        content = pd.read_excel( readinging_path,sheet_name=each )
        content['姓名']=each
        content.dropna(how='any',inplace=True)
        temp = content.append(temp)
    return temp

def sql_rl(  ):
    content = convertion_R_L()
    content.columns = ['A_01', 'A_10', 'A_11', 'A_12', 'A_13', 'A_14', 'A_15', 'A_16', 'A_17',
       'A_18', 'A_19', 'A_02', 'A_20', 'A_21', 'A_22', 'A_23', 'A_24', 'A_25',
       'A_26', 'A_27', 'A_28', 'A_29', 'A_03', 'A_30', 'A_31', 'A_32', 'A_33',
       'A_34', 'A_35', 'A_36', 'A_37', 'A_38', 'A_39', 'A_04', 'A_40', 'A_05',
       'A_06', 'A_07', 'A_08', 'A_09', '刷题材料', '姓名', '日期', '科目']
    sorted = content.columns.tolist()
    sorted.sort( )
    #print(sorted)
    content = content[sorted]
    content.reset_index(drop=True,inplace=True)
    result=[]
    for each in range(len(content)):
        temp = academic_result(content.iloc[each,:].drop( index=['刷题材料','姓名','日期','科目'] ).value_counts()['对'])
        result.append( temp )

    content['总分']=result
    content.replace( '对',True,inplace=True )
    content.replace('错',False,inplace=True )
    print( 'convertion succeeded\n' )

    from database_managment import db_connection

    con = db_connection.connect()

    value = content.values
    sql = '''
                    insert into correction_rl ( test_date,material,student_name,type,band,
                    a01,a02,a03,a04,a05,a06,a07,a08,a09,a10,
                    a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,
                    a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,
                    a31,a32,a33,a34,a35,a36,a37,a38,a39,a40
                        ) values ( %s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                    '''

    cur = con.cursor()
    for each in value:
        cur.execute(sql, ( str(each[-3]),str(each[-5]),str(each[-4]),str(each[-2]),str(each[-1]),str(each[0]),
str(each[1]),
str(each[2]),
str(each[3]),
str(each[4]),
str(each[5]),
str(each[6]),
str(each[7]),
str(each[8]),
str(each[9]),
str(each[10]),
str(each[11]),
str(each[12]),
str(each[13]),
str(each[14]),
str(each[15]),
str(each[16]),
str(each[17]),
str(each[18]),
str(each[19]),
str(each[20]),
str(each[21]),
str(each[22]),
str(each[23]),
str(each[24]),
str(each[25]),
str(each[26]),
str(each[27]),
str(each[28]),
str(each[29]),
str(each[30]),
str(each[31]),
str(each[32]),
str(each[33]),
str(each[34]),
str(each[35]),
str(each[36]),
str(each[37]),
str(each[38]),
str(each[39]) ))

    cur.close()
    con.commit()
    con.close()

