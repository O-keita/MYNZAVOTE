from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from registration import Registration, Login, Vote
from sqlalchemy import func  # Import func

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
    user_id = db.Column(db.String(50), primary_key=True, unique=True)


class Results(db.Model):

    __tablename__ = "Results"
    candidate = db.Column(db.String(50), primary_key=True)
    votes = db.Column(db.Integer, default=0)


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



@app.route("/results")
def results():

    

    with app.app_context():

        results = Results.query.all()

        total_votes = db.session.query(func.sum(Results.votes)).scalar()

        

    return render_template("results.html", title="Results", results = results, total_votes= total_votes)



@app.route("/vote", methods=['GET', 'POST'])
def vote():
    form = Vote()

    if form.validate_on_submit():

        with app.app_context():

            candidate_in_db = Results.query.filter_by(candidate= form.candidate.data).first()

            id_already_in_db = Voters.query.filter_by( user_id = form.user_id.data).first()

            if candidate_in_db:


                if id_already_in_db:


                    flash(f"Voters ID {form.user_id.data} has already voted", "flash_error")

                else:

                    voters = Voters(
                        user_id = form.user_id.data
                    )

                    db.session.add(voters)

                    candidate_in_db.votes +=1

                    flash(f"Successfully Voted for {form.candidate.data} ", "flash_message")

            else:

                results = Results(
                    candidate = form.candidate.data,
                    votes = 1
                )

                db.session.add(results)


                




            db.session.commit()

        
        return redirect(url_for('home'))


    return render_template("vote.html", title="Vote", form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
