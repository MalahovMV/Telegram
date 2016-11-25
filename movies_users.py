from peewee import *
from playhouse.fields import ManyToManyField

db = SqliteDatabase('MoviesUsers.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = IntegerField()

class Movie(BaseModel):
    name = CharField()
    users = ManyToManyField(User,related_name='movies')

def add_movie(name_film):
    query = Movie.select().where(Movie.name == name_film)
    if query.exists():
        print("Данный фильм уже есть в базе")
    else:
        some_film = Movie.create(name=name_film)
        some_film.save()

def len_db_us():
    return len(list(User))

def add_user():
    query = User.select().where(User.user_id == len_db_us())
    if query.exists():
        print("Данный пользователь уже есть в базе")
    else:
        some_user = User.create(user_id=len_db_us())
        some_user.save()

def add_user_per_ind(index):
    query = User.select().where(User.user_id == index)
    if query.exists():
        print("Данный пользователь уже есть в базе")
    else:
        some_user = User.create(user_id=index)
        some_user.save()

def print_films():
    for film in Movie.select():
        print('%s ' % (str(film.name)))

def print_user():
    for user in User.select():
        print('%s ' % user.user_id)


MovieUser = Movie.users.get_through_model()
def createModel():
    if Movie.table_exists():
        print("уже существую")
    else:
        db.create_tables([
            User,
            Movie,
            MovieUser])

createModel()
add_movie(name_film='awd')
add_movie(name_film='awd1')
add_movie(name_film='awd2')
add_movie(name_film='awd3')
add_user_per_ind(100)
add_user_per_ind(99)
add_user_per_ind(98)
add_user_per_ind(97)


def add_id_to_us(id_user,movie_name):
    query_film = Movie.select().where(Movie.name == movie_name)
    if query_film.exists():
        film = Movie.get(Movie.name == movie_name)
        query_us = User.select().where(User.user_id == id_user)
        if query_us.exists():
            user = User.get(User.user_id == id_user)
            if (user in film.users):
                print("Произведена попытка добавить юзера, имеющегося в списке юзеров для данного фильма")
            else:
                film.users.add(user)
        else:
            print("Такого юзера в базе нет, добавь его сначала в базу")
    else:
        print("произведена попытка добавления юзера по несущ фильму")

add_id_to_us(99,'awd')
add_id_to_us(99,'awd1')
add_id_to_us(99,'awd5')
add_id_to_us(100,'awd3')
add_id_to_us(98,'awd2')
add_id_to_us(97,'awd1')
add_id_to_us(898,'awd1')



def print_id_users_by_film(movie_name):
    film = Movie.get(Movie.name == movie_name)
    print(film.name,'используется у: ')
    print([User.user_id for User in film.users])

def view_connect_film_users():
    for movie in Movie.select():
        print_id_users_by_film(movie.name)
        print('\n')

#print_id_users_by_film('awd')
view_connect_film_users()





