from flask_peewee.admin import Admin

from gistsurfr.app import app, db
from gistsurfr.auth import auth
from gistsurfr.models import User, UserRelationship, UserGithub, UserGistFavorite

admin = Admin(app, auth, branding='Gistsurfr')


auth.register_admin(admin)

admin.register(UserRelationship)
admin.register(UserGithub)
admin.register(UserGistFavorite)
