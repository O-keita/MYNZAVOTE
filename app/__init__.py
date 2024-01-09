from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

 # Import func

app = Flask(__name__)
app.config['SECRET_KEY'] = '9a2ef393b4ac4210650e5071'
csrf = CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

from app import route