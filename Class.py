from peewee import *

db = SqliteDatabase('Film_by_peweee.db')

class Film(Model):
    name_film = CharField()
    film_id = IntegerField(primary_key=True)
    year_release = CharField()
    actors = CharField()
    reit = CharField()
    genre = CharField()

    class Meta:
        database = db # This model uses the "Film_by_peweee.db" database.

class User(Model):
    user_id = CharField(primary_key=True)
    lis_film = CharField()

    class Meta:
        database = db # This model uses the "Film_by_peweee.db" database.
