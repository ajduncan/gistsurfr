from hashlib import md5
import datetime

from flask_peewee.auth import BaseUser
from peewee import *
from peewee import create_model_tables

from gistsurfr.app import app, db, PEEWEE_DB


class BaseModel(Model):
    class Meta:
        database = PEEWEE_DB


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    class Meta:
        db_table = 'gsfr_user'

    def __unicode__(self):
        return self.username

    def following(self):
        return User.select().join(
            UserRelationship, on=UserRelationship.to_user
        ).where(UserRelationship.from_user==self).order_by(User.username)

    def followers(self):
        return User.select().join(
            UserRelationship, on=UserRelationship.from_user
        ).where(UserRelationship.to_user==self).order_by(User.username)

    def is_following(self, user):
        return Relationship.select().where(
            UserRelationship.from_user==self,
            UserRelationship.to_user==user
        ).exists()

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)


class UserRelationship(BaseModel):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')


class UserGithub(BaseModel):
    user = ForeignKeyField(User)
    github_access_token = CharField()

    class Meta:
        db_table = 'gsfr_user_github'

    def __str__(self):
        return self.user.username


class UserFavorite(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User)
    gist = CharField()
    name = CharField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gsfr_user_favorite'


models = [User, UserRelationship, UserGithub, UserFavorite]
create_model_tables(models, fail_silently=True)
