import logging
import logging.config

from gistsurfr.app import app


logging.config.dictConfig(app.config['LOGGING'])
log = logging.getLogger(__name__)
