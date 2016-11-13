import datetime

class User:
    def __init__ (self, login, password):
        self.login = str(login)
        self.password = str(password)
        self.queuefilm = []

    def addfilm(self, film, position=-1):
        if film not in self.queuefilm:
            position -= 1
            if (position == -1) or (position >= len(self.queuefilm)):
                position = len(self.queuefilm) + 1
            film.timetoqueue = datetime.datetime.now()
            self.queuefilm = self.queuefilm[:position] + [film] + self.queuefilm[position  : ]

    def showqueue(self):
        for film in self.queuefilm:
            print('''Фильм {0}, {1} года. Рейтинг на кинопоиске - {2}.
            Место в очереди:{3}'''.format(film.name, film.age, film.reit, str(self.queuefilm.index(film) + 1)))

    def delfilmbyname(self, film):
        position = self.queuefilm.index(film)
        self.queuefilm = self.queuefilm[:position] + self.queuefilm[position + 1: ]

    def delfilm(self):
        self.queuefilm = self.queuefilm[1 : ]

    def changefilmposition(self, film, nextpos = 1):
        if nextpos >= len(self.queuefilm) : nextpos = len(self.queuefilm)
        self.delfilmbyname(film)
        self.queuefilm = self.queuefilm[ : nextpos - 1] + [film] + self.queuefilm[nextpos - 1 : ]

    def sortof(self, param): #reiting and age, timetoqueue?
        flag = True
        if param == 'age':
            flag = False
            for count in range(len(self.queuefilm)):
                for counter in range(len(self.queuefilm) ):
                    if self.queuefilm[count].age < self.queuefilm[counter].age:
                        e = self.queuefilm[count]
                        self.queuefilm[count] = self.queuefilm[counter]
                        self.queuefilm[counter] = e

        if param == 'reit':
            flag = False
            for count in range(len(self.queuefilm) - 1):
                for counter in range(len(self.queuefilm) - 1):
                    if self.queuefilm[count].reit > self.queuefilm[counter].reit:
                        e = self.queuefilm[count]
                        self.queuefilm[count] = self.queuefilm[counter]
                        self.queuefilm[counter] = e

        if flag : return ('Не удалось отсортировать список фильмов по данному параметру')
        else: return self.queuefilm

    def printfilmwithparam(self, param, value):
        flag = True
        lis = []
        for film in self.queuefilm:
            if (param == 'name'):
                if value in film.name:
                    #film.printfilm()
                    lis.append(film)
                    flag = False

            if (param == 'genre'):
                if value in film.genre:
                    #film.printfilm()
                    lis.append(film)
                    flag = False

            if (param == 'actors'):
                s = str(film.actors)
                if (value in film.actors) or (value in s):
                    #film.printfilm()
                    lis.append(film)
                    flag = False

            if param == 'reit':
                if int(value) < film.reit:
                    #film.printfilm()
                    lis.append(film)
                    flag = False

            if param == 'age':
                if int(value) < film.age:
                    #film.printfilm()
                    lis.append(film)
                    flag = False

        if flag:
            return('Не удалось найти фильмы удовлетворяющие критерию')
        else: return lis


class Film:
    def __init__(self, page):
        self.name = str(page['name'])
        self.age = int(page['age'])
        self.actors = list(page['actors'])
        self.reit = float(page['reit'])
        self.genre = list(page['genre'])
        self.timetoqueue = None

    def printfilm(self):
        return('''Фильм {0},
             {1} года. Жанр фильма - {2}.
             Рейтинг на кинопоиске - {3}.
             Главные актеры снявшиеся в фильме: {4}.
                '''.format(self.name, self.age, self.genre, self.reit, self.actors))







