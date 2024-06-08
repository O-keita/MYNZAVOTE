from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(email):

    return RegisteredVoters.query.get(int(email))

class RegisteredVoters(db.Model, UserMixin):
    __tablename__ = 'registeredvoters'
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(100), nullable=False)
    id = db.Column(db.String(50), nullable=False)

    

class Voters(db.Model):
    __tablename__ = 'voters'
    user_id = db.Column(db.String(50), primary_key=True, unique=True)


class Results(db.Model):

    __tablename__ = "Results"
    candidate = db.Column(db.String(50), primary_key=True)
    votes = db.Column(db.Integer, default=0)