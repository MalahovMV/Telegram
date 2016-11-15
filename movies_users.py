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

if Movie.table_exists():
    print("уже существую")
else:
    db.create_tables([
        User,
        Movie,
        MovieUser])

add_movie(name_film='awd')
add_movie(name_film='awd1')
add_movie(name_film='awd2')
add_movie(name_film='awd3')
add_user_per_ind(100)
add_user_per_ind(99)
add_user_per_ind(98)
add_user_per_ind(97)
huey = Movie.get(Movie.name == 'awd')

print_user()
awd = Movie.get(Movie.name == 'awd')
us5 = User.get(User.user_id == 100)
us4 = User.get(User.user_id == 99)
us3 = User.get(User.user_id == 98)
us2 = User.get(User.user_id == 97)
if(us5,us4,us3,us2 in huey.users):
    print("такие ребята уже есть")
else:
    huey.users.add([us5,us4,us3,us2])

print([User.user_id for User in huey.users])







