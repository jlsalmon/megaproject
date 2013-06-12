import os

from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.security import SQLAlchemyUserDatastore, Security
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask import Flask, request, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from megaproject.forms import ExtendedRegisterForm
from config import basedir

__author__ = 'jsalmon'

app = Flask(__name__)
app.config.from_object('config')

# Setup mail extension
mail = Mail(app)

# Setup babel
babel = Babel(app)

# Setup database
db = SQLAlchemy(app)
Base = declarative_base()

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from megaproject.models import User, Role

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)

# Setup OpenID
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from megaproject import views, models

