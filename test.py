from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mysqlp@ssw0rd@localhost:3306/test?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique = True)
    password = db.Column(db.String(32), nullable = False)

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    manager.run()