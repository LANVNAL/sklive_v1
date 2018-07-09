# -*- coding:utf-8 -*-
from flask import Flask
#from createdb import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/sklive?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

