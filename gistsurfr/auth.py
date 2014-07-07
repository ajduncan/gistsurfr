from flask_peewee.auth import Auth

from gistsurfr.app import app, db
from gistsurfr.models import User


auth = Auth(app, db, user_model=User)
