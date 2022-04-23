from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='../dist/assets')
csrf = CSRFProtect(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import views, models
from app.models import Users, Favourites, Cars 