from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from registration import Registration, Login, Vote

app = Flask(__name__)
app.config['SECRET_KEY'] = '9a2ef393b4ac4210650e5071'
csrf = CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)



class RegisteredVoters(db.Model):
    __tablename__ = 'registeredvoters'
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(50), nullable=False)

    

class Voters(db.Model):
    __tablename__ = 'voters'
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('registeredvoters.email'), nullable=False)


class Results(db.Model):

    __tablename__ = "Results"
    candidate = db.Column(db.String(50), primary_key=True)
    votes = db.Column(db.Integer)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Registration()

    if form.validate_on_submit():
        with app.app_context():
            new_voter = RegisteredVoters(
                email=form.email.data,
                fname=form.fname.data,
                lname=form.lname.data,
                age=form.age.data,
                password = form.password.data
                
            )
            db.session.add(new_voter)
            db.session.commit()

        flash("Successfully registered", "flash_message")
        return redirect(url_for('home'))

    return render_template('form.html', form=form, title="Registration")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        return redirect(url_for('vote'))



    return render_template("login.html", form=form, title="Login")