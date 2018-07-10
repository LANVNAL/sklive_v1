# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import *
from flask_sqlalchemy import SQLAlchemy
from __init__ import  app


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.SmallInteger, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return str({'id': self.id, 'username': self.username})

    def __getitem__(self, item):
        data = {'id': self.id, 'username': self.username}
        return data[item]

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.SmallInteger, primary_key=True)
    sender = db.Column(db.String(64), unique=False)
    message = db.Column(db.Text(999), nullable=False )
    send_time = db.Column(db.String(64), unique=False)

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


def adduser(username,password,contact):
    new_user = User(username=username, password=password,contact=contact)
    db.session.add(new_user)
    db.session.commit()

def post_msg(sender,message,time):
    new_msg = Message(sender=sender,message=message,send_time=time)
    db.session.add(new_msg)
    db.session.commit()

def reply(responder,message,msg_id,time):
    new_reply = Reply(responder=responder,message=message,msg_id=msg_id,reply_time=time)
    db.session.add(new_reply)
    db.session.commit()



def init_db():
    print u'删除所有表'
    db.drop_all()
    print u'创建新表'
    db.create_all()
    print 'Create DB success'
    db.session.commit()
    user_admin = User(username='admin', password='admin',contact='admin')
    user_normal = User(username='test', password='test',contact='test@qq.com')
    db.session.add(user_admin)
    db.session.add(user_normal)
    db.session.commit()
    db.session.close()

