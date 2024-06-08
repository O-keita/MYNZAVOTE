from flask import render_template, url_for, flash, redirect, request
from app import app,db, bcrypt
from app.registration import Registration, Login, Vote, Renew
from app.models import  RegisteredVoters,Voters, Results
from sqlalchemy import func 
import random
from flask_login import login_user, current_user, logout_user,login_required
import json
from datetime import date, timedelta


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])


def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'flash_message')
        return redirect(url_for('home'))
    
    form = Registration()

    random_5_digit_number = int(''.join(map(str, random.sample(range(10), 5))))

    

    user_email_in_db = RegisteredVoters.query.filter_by(email=form.email.data).first()

    if form.validate_on_submit():

        if user_email_in_db:

            flash("Email already Registered!", "flash_error")

        else:
            with app.app_context():
                hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                new_voter = RegisteredVoters(
                    email=form.email.data,
                    fname=form.fname.data,
                    lname=form.lname.data,
                    age=form.age.data,
                    password = hash_password,
                    id = random_5_digit_number
                    
                )
                db.session.add(new_voter)
                db.session.commit()

            flash("Successfully registered " + str(random_5_digit_number), "flash_message")
            return redirect(url_for('home'))

    return render_template('form.html', form=form, title="Registration")


@app.route("/login", methods=['GET', 'POST'])

def login():

    if current_user.is_authenticated:
        flash('You are already logged in.', 'flash_message')
        return redirect(url_for('home'))


    form = Login()


    if form.validate_on_submit():
        user = RegisteredVoters.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user)

            return redirect(url_for('vote'))
        
        else:

            flash("Incorrect email or password", "flash_error")



    return render_template("login.html", form=form, title="Login")



@app.route("/results")
def results():

    

    with app.app_context():

        results = Results.query.all()

        total_votes = db.session.query(func.sum(Results.votes)).scalar()

        

    return render_template("results.html", title="Results", results = results, total_votes= total_votes)


@app.route("/vote", methods=['GET', 'POST'])

def vote():

    if current_user.is_authenticated:
        return redirect(url_for("vote"))

    form = Vote()

    if form.validate_on_submit():
        candidate_in_db = Results.query.filter_by(candidate=form.candidate.data).first()
        id_already_in_db = Voters.query.filter_by(user_id=form.user_id.data).first()

        if candidate_in_db:
            if id_already_in_db:
                flash(f"Voters ID {form.user_id.data} has already voted", "flash_error")
            else:
                voters = Voters(user_id=form.user_id.data)
                db.session.add(voters)
                candidate_in_db.votes += 1
                flash(f"Successfully Voted for {form.candidate.data}", "flash_message")
        else:
            results = Results(candidate=form.candidate.data, votes=1)
            db.session.add(results)

        db.session.commit()

        return redirect(url_for('home'))

    return render_template("vote.html", title="Vote", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))



@app.route('/renew', methods=['GET', 'POST'])
def renew():
    form = Renew()

    if form.validate_on_submit():
        form_data = form.data
        form_data_str = json.dumps(form_data)  

        
        return redirect(url_for("newvoters", form_data=form_data_str))

    return render_template("renew.html", title='Renew', form=form)



@app.route('/newvoters')
def newvoters():
    current_date = date.today()
    expired_date = current_date + timedelta(5*365)

    random_5_digit_number = int(''.join(map(str, random.sample(range(10), 5))))

    form_data_str = request.args.get('form_data')
    
    form_data = json.loads(form_data_str) if form_data_str else {}

    form = Renew(data=form_data)

    return render_template('newvoters.html', form=form, issue_date=current_date, expired_date=expired_date, new_id = random_5_digit_number)



@app.route('/about')
def about():
    return render_template('about.html')