# flask-github values
GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_CALLBACK_URL = 'http://localhost:5000/github-callback'

DATABASE = {
    'name': 'gistsurfr.db',
    'engine': 'peewee.SqliteDatabase',
    'check_same_thread': False,
}

SECRET_KEY = 'lolol'

DEBUG = True

LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/gsfr.log',
            'maxBytes': 104857600,
            'backupCount': 5,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
        },
        'api': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'ERROR',
        },
        'peewee': {
            'level':'INFO',
        },
    },
}
