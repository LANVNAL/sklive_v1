from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from qz_info import login,userinfo,curriculum,grade,exam_arrangement


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/database'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    func = SelectField('select function', choices=[('info', 'userinfo'), ('exam', 'exam'),('grade','grade'),('curriculum','curriculum')])
    semester = SelectField('select semester',choices=[('2017-2018-1','2017-2018-1'),('2017-2018-2','2017-2018-2'),('2018-2019-1','2018-2019-1'),('2018-2019-2','2018-2019-2')])
    username = StringField('Input your username', validators=[DataRequired()])
    password = StringField('Input your password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserinfoForm(FlaskForm):
    username = StringField('Input your username', validators=[DataRequired()])
    password = StringField('Input your password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/qz')
def qz():
    username = '201601060210'
    password = 'skctf2018'
    semester = '2017-2018-2'
    week = '12'
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    info = userinfo(username,headers,data)
    return render_template('qz.html',info = info)


def get_info(username,password):
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    info = userinfo(username, headers, data)
    return info

def get_exam(username,password):
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    info = exam_arrangement(username,headers,data)
    return info


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        func = form.func.data
        semster = form.semester.data
        username = form.username.data
        password = form.password.data
        if func == 'info':
            info = userinfo(username, password)
        elif func == 'exam':
            info = exam_arrangement(username, password)
        elif func == 'grade':
            info = grade(username,password,semster)
        print type(info),info
        return render_template('qz.html',info = info)
    else:
        return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user', methods=['GET', 'POST'])
def user():
    form = UserinfoForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        info = userinfo(username, password)
        #print type(info),info
        return render_template('userinfo.html',info = info)
    else:
        return render_template('user.html', form=form, name=session.get('name'))

app.run(host='0.0.0.0')


