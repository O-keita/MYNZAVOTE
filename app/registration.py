from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, ValidationError
from app.models import RegisteredVoters



class Registration(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Name"})
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField("Email Adress", validators=[DataRequired()])
    age = IntegerField("Your age", validators=[DataRequired(), NumberRange(min= 18, max=100)])
    password= PasswordField("Set Password", validators=[DataRequired()] )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")


def email_validation(self, email):

    user_email = RegisteredVoters.query.filter_by(email=email.data).first()

    if user_email:

        raise ValidationError("You already have an account")




class Login(FlaskForm):
    email = EmailField("Email Adress", validators=[DataRequired()])
    password= PasswordField("Password", validators=[DataRequired()] )
    submit = SubmitField("Login")



class Vote(FlaskForm):

    choice = ["Omar","Nelson", "Kevin", "Patric"]
    user_id = StringField("Unique ID", validators=[DataRequired(), Length(min=8, max=8)], render_kw={"placeholder": "Unique ID"} )
    candidate = SelectField("Candidate", choices=choice, validators=[DataRequired()], render_kw={"placeholder": "Your Candidate"})
    submit =SubmitField("Vote")


class Renew(FlaskForm):
    fname = StringField("Your First Name", validators=[DataRequired(), Length(min=2, max=70)])
    lname = StringField("Your Second Name", validators=[DataRequired(), Length(min=2, max=70)])
    adress = StringField("Your adress", validators=[DataRequired()])
   
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=18, max=100)])
    old_id = StringField("Your old ID", validators=[Length(min=8, max=8), DataRequired()])
    country = StringField("Country", validators=[DataRequired(), Length(min=2, max=70)])
    submit =SubmitField("Renew")
