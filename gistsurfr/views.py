import os
from random import randint

from flask import Flask, g, redirect, render_template, render_template_string, request, send_from_directory, session, url_for
from flask_github import GitHubError
from flask_peewee.auth import Auth

from gistsurfr.app import app, PEEWEE_DB
from gistsurfr.auth import auth
from gistsurfr.github import github
from gistsurfr.models import User, UserGithub, UserGistFavorite



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
	user_github = None
	user = auth.get_logged_in_user()

	if user is not None:
		user_github = UserGithub.select().where(UserGithub.user == user).first()

	if user_github is not None:
		return user_github.github_access_token
	else:
		return None


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
    	github_user = UserGithub(user=user, github_access_token=access_token)
    	github_user.save()
    	# a more clever way than the above should be used perhaps.
    	auth.login_user(user)
    	gh_user = github.get('user')
    	user.username=str(gh_user['login'])
    	user.email=str(gh_user['email'])
    	user.save()
    else:
    	# user_count = UserGithub.select().where((UserGithub.user == user) & (UserGithub.github_access_token == access_token)).count()
    	github_user = UserGithub.select().where(UserGithub.user == user).first()
    	if github_user is None:
    		github_user = UserGithub(user=user, github_access_token=access_token)
    		github_user.save()

    	if github_user.github_access_token != access_token:
    		github_user.github_access_token = access_token
    		github_user.save()

    return redirect(url_for('index'))


@app.route('/authorize')
def authorize():
    user = auth.get_logged_in_user()

    if user is None:
        return github.authorize()
    else:
        return redirect(url_for('index'))


@app.route('/account')
@auth.login_required
def account():
	gh_user = github.get('user')
	return render_template('gistsurfr/account.html', user=gh_user)


@app.route('/random')
@auth.login_required
def random_gist():
	while True:
		try:
			url = 'gists/{0}'.format(randint(1, 999999))
			gist = github.get(url)
			break
		except GitHubError:
			pass

	return render_template('gistsurfr/random.html', gist=gist)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
