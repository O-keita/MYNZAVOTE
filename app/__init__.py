from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


 # Import func

app = Flask(__name__)
app.config['SECRET_KEY'] = '9a2ef393b4ac4210650e5071'
csrf = CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://omar:mansaring@localhost/Nzavote"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager =LoginManager(app)

from app import route