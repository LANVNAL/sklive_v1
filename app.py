# -*- coding:utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash,Response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,TextAreaField,PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from funcs import login,userinfo,curriculum,grade,exam_arrangement,express,logincheck
from createdb import *
from flask import make_response
import  json,time
from __init__ import app
from captcha import get_answer,get_captcha,get_file,check_captcha
import hashlib
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

bootstrap = Bootstrap(app)
moment = Moment(app)

#init_db()

class NameForm(FlaskForm):
    func = SelectField('select function', choices=[('info', 'userinfo'), ('exam', 'exam'),('grade','grade'),('curriculum','curriculum')])
    semester = SelectField('select semester',choices=[('2017-2018-1','2017-2018-1'),('2017-2018-2','2017-2018-2'),('2018-2019-1','2018-2019-1'),('2018-2019-2','2018-2019-2')])
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = PasswordField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserinfoForm(FlaskForm):
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = PasswordField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GradeForm(FlaskForm):
    semester = SelectField(u'选择学期',choices=[('2017-2018-1','2017-2018-1'),('2017-2018-2','2017-2018-2'),('2018-2019-1','2018-2019-1'),('2018-2019-2','2018-2019-2'),('2019-2020-1','2019-2020-1'),('2019-2020-2','2019-2020-2')])
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = PasswordField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Exam_arrangementForm(FlaskForm):
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = PasswordField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CurriculumForm(FlaskForm):
    semester = SelectField(u'选择学期', choices=[('2017-2018-1', '2017-2018-1'), ('2017-2018-2', '2017-2018-2'),('2018-2019-1', '2018-2019-1'), ('2018-2019-2', '2018-2019-2'),('2019-2020-1', '2019-2020-1'), ('2019-2020-2', '2019-2020-2')])
    week = SelectField(u'选择周数', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16')])
    username = StringField(u'输入学号', validators=[DataRequired()])
    password = PasswordField(u'输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ExpressForm(FlaskForm):
    company = SelectField(u'请选择快递公司',choices=[('yuantong',u'圆通'),('shentong',u'申通')])
    number = StringField(u'请输入运单号', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CheckloginForm(FlaskForm):
    username = StringField(u'输入用户名', validators=[DataRequired()])
    password = PasswordField(u'输入密码', validators=[DataRequired()])
    capcode = StringField(u'输入验证码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField(u'设置用户名', validators=[DataRequired()])
    password = PasswordField(u'设置密码', validators=[DataRequired()])
    qq_or_tel = StringField(u'请输入联系方式QQ或电话', validators=[DataRequired()])
    safe_ques1 = StringField(u'输入你最喜欢的电影（用于密码找回）', validators=[DataRequired()])
    safe_ques2 = StringField(u'输入你最喜欢的歌曲（用于密码找回）', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PassResetForm(FlaskForm):
    username = StringField(u'输入用户名', validators=[DataRequired()])
    safe_ques_num = SelectField(u'选择你的安全问题', choices=[('1','你最喜欢的电影是'),('2','你最喜欢的歌曲是')])
    safe_ques = StringField(u'输入你的答案(安全问题)', validators=[DataRequired()])
    newpassword = PasswordField(u'设置你的新密码', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Post_msg_Form(FlaskForm):
    title = StringField('Your Title',validators=[DataRequired()])
    message = TextAreaField('say somethings',validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReplyForm(FlaskForm):
    message = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    #print session   #测试
    msg = Message.query.filter_by(delect='no').all()
    return render_template('index.html',msg=msg)


@app.route('/captcha', methods=['POST', 'GET'])
def captcha():
    image = file(os.path.join(os.path.dirname(__file__), 'captcha', 'jpgs','ques{}.jpg').format(session['uuid']))
    return Response(image, mimetype='image/jpeg')

@app.route('/login',methods=['GET', 'POST'])            #SKlive的登陆
def login():
    #checkform = CheckloginForm()
    #print session
    if 'login' in session and session['login'] == True:
        flash("你已经登陆")
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            captcha_judge = check_captcha(request.form.get('captcha_x'), request.form.get('captcha_y'), session['uuid'])
        except:
            captcha_judge = False
        if 'username' not in session:
            session['login'] = False
            session['login_error'] = 0
            session['username'] = ''
        if session['login'] == True:
            return render_template('welcome.html',name = session['username'], error = 0)
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if not user or user.password != password:
                session['login_error'] += 1
                flash("用户名或密码错误")
                captcha_list = get_captcha()
                session['uuid'] = captcha_list[0]
                return render_template('login.html',uuid=captcha_list[0],ques=captcha_list[1].decode('utf-8'),login_error=session['login_error'])
            if not captcha_judge and session['login_error'] >= 3:
                flash("验证码错误!")
                captcha_list = get_captcha()
                session['uuid'] = captcha_list[0]
                return render_template('login.html',uuid=captcha_list[0],ques=captcha_list[1].decode('utf-8'),login_error=session['login_error'])
            else:
                session['login'] = True
                session['username'] = username
                session['login_error'] = 0
                if username == 'admin':
                    session['admin'] = True
                else:
                    session['admin'] = False
                return render_template('welcome.html',name = username, error = 0)
    else:
        captcha_list = get_captcha()
        session['uuid'] = captcha_list[0]
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash(u"已成功登出")
    #session['login'] = False
    session.clear()
    return redirect(url_for('login'))

@app.route('/register',methods=['GET', 'POST'])         #SKlive的注册
def register():
    form = RegisterForm()
    if 'username' not in session:
        session['login'] = False
    if session['login'] == True:
        flash("你已经登陆，如需注册请先登出！")
        return redirect(url_for('index'))
        #return render_template('welcome.html', name=session['username'], error=0)
    else:
        if form.validate_on_submit():
            username = form.username.data
            password = hashlib.md5(form.password.data).hexdigest()
            contact = form.qq_or_tel.data
            safe_ques1 = form.safe_ques1.data
            safe_ques2 = form.safe_ques2.data
            user = User.query.filter_by(username=username).first()
            if user:
                flash("用户已存在")
                return render_template('register.html', form=form)
            else:
                adduser(username,password,contact,safe_ques1,safe_ques2)
                session['login'] = True
                session['username'] = username
                return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)


@app.route("/pass/reset",methods=['GET', 'POST'])   #密码重置
def reset():
    form = PassResetForm()
    if form.validate_on_submit():
        username = form.username.data
        newpassword = form.newpassword.data
        safe_ques_num = form.safe_ques_num.data
        safe_ques = form.safe_ques.data
        user = User.query.filter_by(username=username).first()
        if safe_ques_num == 1:              #选择安全问题
            answer = user.safe_ques1
        else:
            answer = user.safe_ques2
        if 'rst_error_time' in session and time.time()-session['rst_error_time']<30:    #限制30秒提交一次
            flash("请{}秒后重试".format(int(30-(time.time()-session['rst_error_time']))))
        else:
            if safe_ques == answer:
                reset_password(username,newpassword)
                session['login'] = False
                return redirect(url_for('login'))
            else:
                flash(u"安全问题答案错误")
                session['rst_error_time'] = time.time()
                return render_template('reset.html',form=form)
    return render_template('reset.html', form=form)



@app.route('/skuser/<username>',methods=['GET', 'POST'])
def user_information(username):
    if 'username' not in session:
        session['login'] = False
    if session['login'] == True:
        user = User.query.filter_by(username=username).first()
        contact = user.contact
        msg = Message.query.filter_by(sender=username).all()
        return render_template('skuser.html',username=username,contact=contact,msg=msg)
    else:
        flash(u"请登录")
        return redirect(url_for('login'))


@app.route('/message/<msg_id>',methods=['GET', 'POST'])
def msg_detail(msg_id):
    if 'username' not in session:
        session['login'] = False
    if session['login'] == True:
        form = ReplyForm()
        msg = Message.query.filter_by(id=msg_id).first()
        replies = Reply.query.filter_by(msg_id=msg_id).all()
        now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        if form.validate_on_submit():
            reply_msg = form.message.data
            responder = session['username']
            reply(responder,reply_msg,msg_id,now_time)
            #return render_template('message.html',form=form,msg=msg,replies=replies)
            return redirect(url_for('msg_detail',msg_id=msg_id))
        else:
            return render_template('message.html', form=form, msg=msg, replies=replies)
    else:
        return redirect(url_for('login'))


@app.route('/delect/<msg_id>',methods=['GET','POST'])
def msg_delect(msg_id):
    if 'username' not in session:
        session['login'] = False
    if session['login'] == True and session['username'] == 'admin':
        #msg = Message.query.filter_by(id=msg_id).first()
        delect_msg(msg_id)
    else:
        flash(u"无权访问！！")
    return redirect(url_for('index'))



@app.route('/post',methods=['GET', 'POST'])         #发帖
def postmsg():
    if 'username' not in session:
        session['login'] = False
    if session['login'] == True:
        form = Post_msg_Form()
        if form.validate_on_submit():
            sender = session['username']
            title = form.title.data
            msg = form.message.data
            post_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            post_msg(sender,title,msg,post_time)
            return redirect(url_for('index'))
        else:
            return render_template('postmsg.html',form=form)
    else:
        flash(u"请登录")
        return redirect(url_for('login'))




@app.route('/user', methods=['GET', 'POST'])        #强智的用户信息查询
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



@app.route('/app/<name>',methods=['GET','POST'])    #给安卓应用的接口
def api(name):
    if name == 'logincheck':
        getjson = request.get_data()
        data = json.loads(getjson)
        #userinfo = re.findall('username:(\w+),password:(\w+)',data)
        username = data['username']
        password = data['password']
        check = logincheck(username, password)
        if check == 'ok':
            return 'ok'
        else:
            return  'error'
    if name == 'userinfo':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        check = logincheck(username,password)
        if check != 'ok':
            return 'error'
        else:
            info = userinfo(username,password)
            return  str(info)
    if name == 'grade':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        semester = data['semester']
        check = logincheck(username,password)
        if check != 'ok':
            return 'error'
        else:
            info = grade(username,password,semester)
            return str(info)
    if name == 'exam':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        check = logincheck(username,password)
        if check != 'ok':
            return 'error'
        else:
            info = exam_arrangement(username, password)
            return str(info)
    if name == 'curriculum':
        getjson = request.get_data()
        data = json.loads(getjson)
        username = data['username']
        password = data['password']
        semester = data['semester']
        week = data['week']
        check = logincheck(username, password)
        if check != 'ok':
            return 'error'
        else:
            info = curriculum(username, password, semester,week)
            return str(info)
    if name == 'express':
        getjson = request.get_data()
        data = json.loads(getjson)
        company = data['company']
        number = data['number']
        info = exam_arrangement(company, number)
        if info['status'] == '200':
            return str(info)
        else:
            return 'error'


app.run(host='0.0.0.0')