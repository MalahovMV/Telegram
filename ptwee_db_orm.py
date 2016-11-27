from peewee import *

db = SqliteDatabase('Film_by_peweee.db')

class Film(Model):
    name_film = CharField()
    film_id = IntegerField(primary_key=True)
    year_release = CharField()
    actors = CharField()
    reit = CharField()
    genre = CharField()
    user_id = CharField()

    class Meta:
        database = db # This model uses the "Film_by_peweee.db" database.

def add_film(name_film , film_id, year_release, actors, reit, genre, user_id):
    some_film = Film.create(name_film=name_film,film_id=film_id,year_release=year_release,
                            actors=actors,reit=reit,
                            genre=genre, user_id=user_id)
    some_film.save()

def del_film(name):
    for film in Film.select():
        if film.name_film == name:
            film.delete_instance()

def print_films():
    film_name = ''
    for film in Film.select():
        print('%s. %s. %s. %s. %s. %s. %s.' % (film.name_film, film.film_id, film.year_release, film.actors, film.reit, film.genre, film.user_id))
        film_name += film.name_film

    return film_name

def film_in(name, age, user_id):
    flag = False
    for film in Film.select():
        if (film.name_film == name) and (film.year_release == age):
            flag = True
            break

    if flag:
        film.user_id += ' ,' + user_id
        return True

    else:
        return False

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



