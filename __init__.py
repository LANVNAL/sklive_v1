# -*- coding:utf-8 -*-
from flask import Flask
#from createdb import init_db
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xxx@localhost:3306/test?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

