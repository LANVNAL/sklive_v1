# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import *
from flask_sqlalchemy import SQLAlchemy
from __init__ import  app


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.SmallInteger, primary_key=True)
    username = db.Column(db.String(64), unique=True)        #设置位只有用户名不允许重复
    password = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(64), unique=False)
    safe_ques1 = db.Column(db.String(64), unique=False)
    safe_ques2 = db.Column(db.String(64), unique=False)

    def __repr__(self):
        return str({'id': self.id, 'username': self.username})

    def __getitem__(self, item):
        data = {'id': self.id, 'username': self.username}
        return data[item]

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.SmallInteger, primary_key=True)
    sender = db.Column(db.String(64), unique=False)
    title = db.Column(db.String(64),unique=False)
    message = db.Column(db.Text(999), nullable=False )
    send_time = db.Column(db.String(64), unique=False)
    delect = db.Column(db.String(6), unique=False)

    def __repr__(self):
        return str({'id': self.id, 'sender': self.sender})

    def __getitem__(self, item):
        data = {'id': self.id, 'sender': self.sender}
        return data[item]


class Reply(db.Model):
    __yablename__ = 'reply'
    id = db.Column(db.SmallInteger,primary_key=True)
    responder = db.Column(db.String(64), unique=False)
    message = db.Column(db.Text(999), nullable=False)
    msg_id = db.Column(db.SmallInteger,unique=False)
    reply_time = db.Column(db.String(64), unique=False)

    def __repr__(self):
        return str({'id': self.id, 'responder': self.responder})

    def __getitem__(self, item):
        data = {'id': self.id, 'responder': self.responder}
        return data[item]


def adduser(username,password,contact,safe_ques1,safe_ques2):
    new_user = User(username=username, password=password, contact=contact, safe_ques1=safe_ques1, safe_ques2=safe_ques2)
    db.session.add(new_user)
    db.session.commit()

def reset_password(username,newpassword):
    User.query.filter_by(username=username).update({'password':newpassword})
    db.session.commit()

def post_msg(sender,title,message,time):
    new_msg = Message(sender=sender,title=title,message=message,send_time=time,delect='no')
    db.session.add(new_msg)
    db.session.commit()

def reply(responder,message,msg_id,time):
    new_reply = Reply(responder=responder,message=message,msg_id=msg_id,reply_time=time)
    db.session.add(new_reply)
    db.session.commit()

def delect_msg(msg_id):
    Message.query.filter_by(id=msg_id).update({'delect':'yes'})
    db.session.commit()



def init_db():
    print u'删除所有表'
    db.drop_all()
    print u'创建新表'
    db.create_all()
    print 'Create DB success'
    db.session.commit()
    user_admin = User(username='admin', password='21232f297a57a5a743894a0e4a801fc3',contact='admin',safe_ques1='a', safe_ques2='b')
    user_normal = User(username='test', password='098f6bcd4621d373cade4e832627b4f6',contact='test@qq.com',safe_ques1='s',safe_ques2='s')
    db.session.add(user_admin)
    db.session.add(user_normal)
    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    init_db()
