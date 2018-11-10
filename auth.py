from flask import Flask,Blueprint,render_template,request,redirect,url_for

admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_login( ):
    return render_template( 'welcome.html' )


@admin.route('/login',methods=['POST','GET'])
def auth( ):
    if request.method=='GET':
        name = request.args.get( 'admin_name','' )
        pwd = request.args.get('password', '')
        if name=='admin' and pwd=='admin':
            return 'secceed'
        else:
            return redirect( url_for(admin_login) )
    else:
        return redirect(url_for(admin_login))

app=Flask( __name__ )
app.register_blueprint( admin,url_prefix='/admin' )

app.route('/')
def index():
    return 'this is the page!'
app.run()
