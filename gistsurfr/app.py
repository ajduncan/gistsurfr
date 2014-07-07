from flask import Flask
from flask_peewee.db import Database
from peewee import SqliteDatabase

PEEWEE_DB = SqliteDatabase(None)


app = Flask(__name__)
app.config.from_object('gistsurfr.settings')

PEEWEE_DB.init(
    app.config['DATABASE']['name'],
)

db = Database(app)
