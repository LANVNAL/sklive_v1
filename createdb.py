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

    def __repr__(self):
        return str({'id': self.id, 'username': self.username})

    def __getitem__(self, item):
        data = {'id': self.id, 'username': self.username}
        return data[item]



def adduser(username,password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()


def init_db():
    print u'删除所有表'
    db.drop_all()
    print u'创建新表'
    db.create_all()
    print 'Create DB success'
    db.session.commit()
    user_admin = User(username='admin', password='admin')
    user_normal = User(username='test', password='test')
    db.session.add(user_admin)
    db.session.add(user_normal)
    db.session.commit()
    db.session.close()

