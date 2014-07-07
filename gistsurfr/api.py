from flask_peewee.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication, RestrictOwnerResource

from gistsurfr.app import app
from gistsurfr.auth import auth
from gistsurfr.models import User, UserRelationship, UserGithub, UserFavorite


user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)


class UserResource(RestResource):
	exclude = ('password', 'email',)


class UserRelationshipResource(RestResource):
	exclude = ()


class UserGithubResource(RestResource):
	exclude = ('github_access_token',)


class FavoriteResource(RestResource):
    def prepare_data(self, obj, data):
        return data


# register our models so they are exposed via /api/<model>/
api.register(User, UserResource, auth=admin_auth)
api.register(UserGithub, UserGithubResource, auth=admin_auth)
api.register(USerRelationship, UserRelationshipResource, auth=user_auth)
api.register(UserFavorite, FavoriteResource, auth=user_auth)
