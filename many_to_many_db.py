from sqlalchemy import create_engine
import os

if os.path.exists("some.db"):
    os.remove("some.db")
e = create_engine("some.db")
e.execute("""
    create table Users (
        user_id integer primary key,
        name varchar
    )
""")
e.execute("""
    create table Films (
        film_id integer primary key,
        title varchar
    )
""")

e.execute("""
    create table UsersMovies (
        User_id integer,
        Movie_id integer,

    )
""")

