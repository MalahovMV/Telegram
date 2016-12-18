from peewee import *
from Class import Film,User

db = SqliteDatabase('Film_by_peweee.db')


def add_user(user_id):
    user = User.select().where(User.user_id == user_id)
    if not user:
        user = User.create(user_id=user_id, lis_film='')
        user.save()

def add_film(name_film , film_id, year_release, actors, reit, genre):
    some_film = Film.create(name_film=name_film,film_id=film_id,year_release=year_release,
                            actors=actors,reit=reit,
                            genre=genre)
    some_film.save()

def add_film_user(name, age, user_id):
    for user in User.select().where(User.user_id == user_id):
        for film in Film.select().where((Film.name_film == name) and (Film.year_release == age)):
            if not (str(film.film_id) in user.lis_film):
                if user.lis_film:
                    user.lis_film += ',' + str(film.film_id)

                else:
                    user.lis_film += str(film.film_id)

                user.save()

def del_film(user_id, name, age):
    for user in User.select().where(User.user_id == user_id):
        film_lis = str(user.lis_film)
        film_lis = film_lis.split(',')
        nam =''
        for film_id in film_lis:
            for film in Film.select().where(Film.film_id == int(film_id)):
                if ((name in film.name_film) and (film.year_release == age)):
                    nam = name
                    id = film_id

        film_lis = film_lis[:film_lis.index(id)] + film_lis[film_lis.index(id) + 1:]
        lis_film =''
        for film in film_lis:
            lis_film += str(film) + ','

        lis_film = lis_film[:-1]
        user.lis_film = lis_film
        user.save()

    return nam

def print_films(user_id):
    film_lis = []
    for user in User.select().where(User.user_id == user_id):
        movie_lis = str(user.lis_film)
        movie_lis = movie_lis.split(',')
        film_lis = []
        for film_id in movie_lis:
            for film in Film.select().where(Film.film_id == film_id ):
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
    for user in User.select().where(User.user_id == user_id):
        name = print_films(user_id)[0]
        try:
            user.lis_film = user.lis_film[2:]

        except:
            user.lis_film = ''

        user.save()

    return name

def return_up_age(user_id, age):
    film_list =[]
    for user in User.select().where(User.user_id == user_id):
        film_lis = str(user.lis_film).split(',')
        for film_id in film_lis:
            for film in Film.select().where(Film.film_id == film_id):
                if film.year_release > age:
                    film_list.append(str(film.name_film + ' ' + film.year_release))

    return film_list

def return_up_reit(user_id, reit):
    film_list = []
    for user in User.select().where(User.user_id == user_id):
        film_lis = str(user.lis_film).split(',')
        for film_id in film_lis:
            for film in Film.select().where(Film.film_id == film_id):
                if film.reit > reit:
                    film_list.append(str(film.name_film + ' ' + film.year_release + ' ' + film.reit))

    return film_list

def change_position(user_id, name, age, pos):
    for user in User.select().where(User.user_id == user_id):
        film_lis = str(user.lis_film)
        film_lis = film_lis.split(',')
        for film_id in film_lis:
            for film in Film.select().where(Film.film_id == int(film_id)):
                if ((name in film.name_film) and (film.year_release == age)):
                    id = film_id

        pos = int(pos) - 1
        if pos >= len(film_lis):
            pos = len(film_lis) - 1

        pos_id = film_lis.index(id)
        if pos_id > pos:
            film_lis = film_lis[:pos] + list(id) + film_lis[pos : pos_id] + film_lis[pos_id +1  :]

        if pos_id < pos:
            film_lis = film_lis[:pos_id]  + film_lis[pos_id + 1: pos + 1] + list(id) + film_lis[pos + 1:]

        lis_film = ''
        for film in film_lis:
            lis_film += str(film) + ','

        lis_film = lis_film[:-1]
        user.lis_film = lis_film
        user.save()

def del_unusable_film():
    set_id = set()
    for user in User.select():
        film_lis = str(user.lis_film)
        film_lis = film_lis.split(',')
        for film_id in film_lis:
                set_id |= set(film_id)

    for film in Film.select():
        if not (str(film.film_id) in list(set_id)):
            film.delete_instance()

    return list(set_id)



