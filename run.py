#!/usr/bin/env python

import logging.config

from gistsurfr.app import app, db
from gistsurfr.log import log
from gistsurfr.auth import auth
from gistsurfr.admin import admin
from gistsurfr.api import api
from gistsurfr.doc import *
from gistsurfr.models import *
from gistsurfr.views import *


admin.setup()
api.setup()


if __name__ == "__main__":
    logging.config.dictConfig(app.config['LOGGING'])

    auth.User.create_table(fail_silently=True)

    admin_count = auth.User.select().where(auth.User.admin == True).count()
    if admin_count == 0:
	    admin_user = auth.User(username=app.config['ADMIN_USERNAME'], email='admin@localhost', admin=True, active=True)
	    admin_user.set_password(app.config['ADMIN_PASSWORD'])
	    admin_user.save()

    app.run(debug=True, host='0.0.0.0', port=5000)
