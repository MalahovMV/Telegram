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

def add_film(name_film,film_id,year_release,actors,reit,genre):
    some_film = Film.create(name_film=name_film,film_id=film_id,year_release=year_release,
                            actors=actors,reit=reit,
                            genre=genre)
    some_film.save()

def del_film(name):
    for film in Film.select():
        if film.name_film == name:
            film.delete_instance()

def print_films():
    film_name = ''
    for film in Film.select():
        print('%s %s %s %s %s %s ' % (film.name_film, film.film_id, film.year_release, film.actors, film.reit, film.genre))
        film_name += film.name_film

    return film_name

def is_checked():
    db.connect()
    if Film.table_exists():
        #print("уже существую, дружище, не создавай новую я же обижусь) ")
        return True
    else:
        db.create_tables([Film])
        return False

def len_db():
    return len(list(Film))

if __name__ == "__main__":
    is_checked()
    print_films()



