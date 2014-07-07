import os

from flask import Flask, g, redirect, render_template, render_template_string, request, send_from_directory, session, url_for
from flask_peewee.auth import Auth

from gistsurfr.app import app, PEEWEE_DB
from gistsurfr.auth import auth
from gistsurfr.github import github
from gistsurfr.models import User, UserGithub, UserFavorite



@app.before_request
def before_request():
    g.db = PEEWEE_DB
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@github.access_token_getter
def token_getter():
    user = auth.get_logged_in_user()
    if user is not None:
        return user.github_access_token


@app.route('/')
def index():
	return render_template('gistsurfr/index.html')


@app.route('/None')
def none():
	return redirect(url_for('index'))


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)

    user = auth.get_logged_in_user()
    if user is None:
    	user = User(username=str(access_token), password=str(access_token), email=str(access_token), admin=False, active=True)
    	user.save()
    	github_user = UserGithub(User=user, github_access_token=access_token)
    	github_user.save()
    	# this is hacky?
    	auth.login_user(user)
    	# user.username=str(github.get('user'))
    	# user.save()
    else:
    	# user_count = UserGithub.select().where((UserGithub.user == user) & (UserGithub.github_access_token == access_token)).count()
    	github_user = UserGithub.select().where(UserGithub.user == user)
    	if github_user is None:
    		github_user = UserGithub(user=user, github_access_token=access_token)
    		github_user.save()
    	else:
    		github_user.github_access_token = access_token
    		github_user.save()

    return redirect(url_for('index'))


@app.route('/github-authorize')
def login():
    user = auth.get_logged_in_user()

    if user is None:
        return github.authorize()
    else:
        return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
