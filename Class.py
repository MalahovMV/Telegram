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

def is_checked():
    db.connect()
    if Film.table_exists():
        pass
    else:
        db.create_tables([Film])

    if User.table_exists():
        pass

    else:
        db.create_tables([User])

if __name__ == '__main__':
    is_checked()