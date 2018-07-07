# -*- coding:utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from funcs import login,userinfo,curriculum,grade,exam_arrangement,express,logincheck
import  json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['JSON_AS_ASCII'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/database'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    func = SelectField('select function', choices=[('info', 'userinfo'), ('exam', 'exam'),('grade','grade'),('curriculum','curriculum')])
    semester = SelectField('select semester',choices=[('2017-2018-1','2017-2018-1'),('2017-2018-2','2017-2018-2'),('2018-2019-1','2018-2019-1'),('2018-2019-2','2018-2019-2')])
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = StringField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserinfoForm(FlaskForm):
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = StringField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GradeForm(FlaskForm):
    semester = SelectField(u'选择学期',choices=[('2017-2018-1','2017-2018-1'),('2017-2018-2','2017-2018-2'),('2018-2019-1','2018-2019-1'),('2018-2019-2','2018-2019-2'),('2019-2020-1','2019-2020-1'),('2019-2020-2','2019-2020-2')])
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = StringField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Exam_arrangementForm(FlaskForm):
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = StringField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CurriculumForm(FlaskForm):
    semester = SelectField(u'选择学期', choices=[('2017-2018-1', '2017-2018-1'), ('2017-2018-2', '2017-2018-2'),('2018-2019-1', '2018-2019-1'), ('2018-2019-2', '2018-2019-2'),('2019-2020-1', '2019-2020-1'), ('2019-2020-2', '2019-2020-2')])
    week = SelectField(u'选择周数', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16')])
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = StringField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ExpressForm(FlaskForm):
    company = SelectField(u'请选择快递公司',choices=[('yuantong',u'圆通'),('shentong',u'申通')])
    number = StringField(u'请输入运单号', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    form = UserinfoForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        check = logincheck(username,password)
        if check == 'ok':
            info = userinfo(username, password)
            loginerror = 0
            return render_template('userinfo.html', info = info, error = loginerror)
        else:
            loginerror = 1
            return render_template('userinfo.html', error=loginerror)
    else:
        return render_template('user.html', form=form, name=session.get('name'))

@app.route('/grade', methods=['GET', 'POST'])
def mygrade():
    form = GradeForm()
    if form.validate_on_submit():
        semester = form.semester.data
        username = form.username.data
        password = form.password.data
        check = logincheck(username, password)
        if check == 'ok':
            info = grade(username, password,semester)
            loginerror = 0
            return render_template('mygrade.html', info = info ,error = loginerror)
        else:
            loginerror = 1
            return render_template('mygrade.html', error=loginerror)
    else:
        return render_template('grade.html', form=form, name=session.get('name'))

@app.route('/exam',methods=['GET', 'POST'])
def myexam():
    form = Exam_arrangementForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        check = logincheck(username, password)
        if check == 'ok':
            info = exam_arrangement(username, password)
            loginerror = 0
            return render_template('myexam.html', info = info, error = loginerror)
        else:
            loginerror = 1
            return render_template('myexam.html', error=loginerror)
    else:
        return render_template('exam.html', form=form, name=session.get('name'))

@app.route('/curriculum',methods=['GET', 'POST'])
def mycurriculum():
    form = CurriculumForm()
    if form.validate_on_submit():
        semester = form.semester.data
        week = form.week.data
        username = form.username.data
        password = form.password.data
        check = logincheck(username, password)
        if check == 'ok':
            info = curriculum(username, password,semester,week)
            loginerror  = 0
            #print type(info),info
            return render_template('mycurriculum.html', info = info, error = loginerror)
        else:
            loginerror = 1
            return render_template('mycurriculum.html', error=loginerror)
    else:
        return render_template('curriculum.html', form=form, name=session.get('name'))

@app.route('/express',methods=['GET', 'POST'])
def myexpress():
    form = ExpressForm()
    if form.validate_on_submit():
        company = form.company.data
        number = form.number.data
        info = express(company,number)
        #print type(info)
        if info['status'] == '200':
            msgerror = 0
        else:
            msgerror = 1
        info = info['data']
        #print type(info)
        return render_template('myexpress.html',info = info,msgerror = msgerror)
    else:
        return render_template('express.html', form=form, name=session.get('name'))



@app.route('/app/<name>',methods=['GET','POST'])
def api(name):
    if name == 'userinfo':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        info = userinfo(username,password)
        return  str(info)
    if name == 'grade':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        semester = data['semester']
        info = grade(username,password,semester)
        return str(info)
    if name == 'exam':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        info = exam_arrangement(username, password)
        return str(info)
    if name == 'curriculum':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        semester = data['semester']
        week = data['week']
        info = curriculum(username, password, semester,week)
        return str(info)
    if name == 'express':
        getjson = request.get_data()
        data = json.loads(getjson)
        company = data['company']
        number = data['number']
        info = exam_arrangement(company, number)
        return str(info)


app.run(host='0.0.0.0')