import sqlite3

def create_connect():
    createDb.commit()

createDb = sqlite3.connect("User's_films.db")
queryCurs = createDb.cursor()

def createTable():
    queryCurs.execute('''create table films (name_film text, year_release text, actors text, reit text,genre text)''')

def addFilm(name_film,year_release,actors,reit,genre):
    queryCurs.execute(''' INSERT INTO films (name_film,year_release,actors,reit,genre) VALUES(?,?,?,?,?)''',(name_film, year_release,actors,reit,genre))

def print_user_s_films():
        queryCurs.execute('SELECT * FROM films  ORDER BY name_film')
        listTittle = ['name_film', 'year_release', 'actors', 'reit', 'genre']
        k = 0
        for i in queryCurs:
            print('\n')
            for j in i:
                if k < 5:
                    print(listTittle[k])
                    print(j)
                    k += 1
                else:
                    k = 0
                    print(listTittle[k])
                    print(j)
                    k += 1

        queryCurs.close()





if __name__ == '__main__':
    createTable()
