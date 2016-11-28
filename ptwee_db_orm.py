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

def del_film(user_id, name, age):
    for film in Film.select().where(Film.user_id == user_id):
        if (film.name_film == name) and (film.year_release == age):
            nam = film.name_film
            film.delete_instance()
            break

    return nam

def print_films(user_id):
    film_lis = []
    for film in Film.select().where(Film.user_id == user_id):
        film_lis.append(str('%s. %s ' % (film.name_film, film.year_release)))

    return film_lis

def return_film(name, age):
    for film in Film.select().where(Film.name_film == name):
        if film.year_release == age:
            text = 'Название: ' + film.name_film + "\nГод выхода: " + film.year_release
            text += "\nРежзисер и актеры: " + film.actors + "\nЖанр: " + film.genre
            text += "\nРейтинг: " + film.reit
            return text

    return False


def film_in(name, age, user_id):
    #flag = False
    #for film in Film.select():
     #   if (film.name_film == name) and (film.year_release == age):
      #      flag = True
       #     break

    #if flag:
     #   film.user_id += ' ,' + user_id
      #  return True

    #else:
    return False

def is_checked():
    db.connect()
    if Film.table_exists():
        #print("уже существую, дружище, не создавай новую я же обижусь) ")
        return True
    else:
        db.create_tables([Film])
        return False

def return_id_film():
    empty_position = find_empty()
    if empty_position:
        return empty_position[0]

    return len(list(Film))

def find_empty():
    id_list = []
    for film in Film.select():
        id_list.append(film.film_id)

    id_list.sort()
    empty_pos = []
    i = 0
    for el in id_list:
        if i == el:
            i += 1

        else:
            while not (i == el) :
                empty_pos.append(i)
                i += 1

    return empty_pos

def pop(user_id):
    for film in Film.select().where(Film.user_id == user_id):
        name = film.name_film
        film.delete_instance()
        break

    return name

def return_up_age(user_id, age):
    film_lis =[]
    for film in Film.select().where(Film.user_id == user_id):
        if film.year_release > age:
            film_lis.append(str(film.name_film + ' ' + film.year_release))

    return film_lis

def return_up_reit(user_id, reit):
    film_lis =[]
    for film in Film.select().where(Film.user_id == user_id):
        if film.reit > reit:
            film_lis.append(str(film.name_film + ' ' + film.year_release + ' ' + 'Reiting: ' + film.reit))

    return film_lis

if __name__ == "__main__":
    is_checked()
    #print_films()
    print(find_empty())
    text = ''
    for film in Film.select():
        text += 'Название: ' + film.name_film + "\nГод выхода: " + film.year_release
        text += "\nРежзисер и актеры: " + film.actors + "\nЖанр: " + film.genre
        text += "\nРейтинг: " + film.reit + "\n User_id = "+ film.user_id + "\n\n"

    print(text)


