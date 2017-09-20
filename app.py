from flask import *
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from db.db_Models import UserAccounts, db, LoginLog, DataLog
import requests
import flask_admin as admin
from db.adminModel import UserAccountsAdmin, LoginLogAdmin, DataLogAdmin, MyView
from functools import wraps


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'secret string'  # Change this!
app.secret_key = 'hahaha'
# app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_pyfile('config.py')
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "Please LOG IN"
login_manager.login_message_category = "info"

admin = admin.Admin(app, name=u'后台管理系统',  index_view= MyView(name=u'首页'),template_mode='bootstrap3')
admin.add_view(UserAccountsAdmin(UserAccounts, db.session, name=u'用户管理'))
admin.add_view(LoginLogAdmin(LoginLog, db.session,name=u'登入日志'))
# admin.add_view(DataLogAdmin(DataLog, db.session))
# admin.add_view(MyView(name='首页'))




def getIPinfo(ip):
    url = 'http://ip.taobao.com//service/getIpInfo.php?ip={}'.format(ip)
    data = requests.get(url)
    if data.status_code == 200:
        print(data.json()['code'])
        print(data.json()['data']['country'])
        print(data.json()['data']['region'])
        print(data.json()['data']['city'])
        print(data.json()['data']['county'])
        print(data.json()['data']['isp'])

def db_add(obj):
    db.session.add(obj)
    db.session.commit()

def query_user(username):
    user = UserAccounts.query.filter_by(UserName=username).first()
    if user:
        return True
    return False

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if query_user(username):
        user = User()
        user.id = username
        return user
    return None


@app.route('/')
@app.route('/index')
@login_required
def index():
    user_id = session.get('user_id')
    # user = UserAccounts.query.filter_by(u=user_id).first()
    # print(user_id)
    # print(current_user.UserName)
    return render_template("index.html", user=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')

    if request.method == 'GET':
        return render_template("login.html")

    if (current_user.is_authenticated and query_user(user_id)):
        return redirect(url_for('index'))

    username = request.form['username']
    user = UserAccounts.query.filter_by(UserName=username).first()
    if user == None:
        return render_template("login.html", error='用户名或密码错误')
    pw_form = request.form['password']
    pw_db = user.Password
    if pw_form == pw_db:
        user = User()
        user.id = username
        login_user(user, remember=True)
        # print('Logged in successfully')
        # flash('Logged in successfully')
        # ip = request.remote_addr
        # lg = LoginLog(username, ip,'')
        # db_add(lg)
        # getIPinfo('112.64.153.115')
        print(current_user)
        return redirect(url_for('index'))

    return render_template("login.html", error='用户名或密码错误')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




if __name__ == '__main__':
    # db.create_all()
    db.init_app(app)
    # db.create_all()
    app.run()
