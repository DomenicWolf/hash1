from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """user model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    username = db.Column(db.String(20),nullable=False,unique=True)

    password = db.Column(db.String,nullable=False)

    email = db.Column(db.String(50),nullable=False,unique=True)

    first_name = db.Column(db.String(30),nullable=False)

    last_name = db.Column(db.String(30),nullable=False)

    @classmethod
    def register(cls,username,pwd,email,first_name,last_name):
        """register user w/hashed pass"""

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username,password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)
    
    @classmethod
    def authenticate(cls,username,pwd):
        """validate that user exists and pass is correct"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False
        
class Feedback(db.Model):
    """feedback model"""
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.String(100),nullable=False)

    content = db.Column(db.Text,nullable = False)

    username = db.Column(db.String,db.ForeignKey('users.username'))

    user = db.relationship('User',backref='feedbacks')

    @classmethod
    def new_feedback(cls,title,content,username):
        return cls(title=title,content=content,username=username)