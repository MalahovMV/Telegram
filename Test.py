from Class import Film, User
import unittest


class FilmTest(unittest.TestCase):
    def setUp(self):
        self.film1 = Film({'name' : 'Властелин колец: Братство Кольца', 'age' : '2001',
                           'actors' : ['Иен Маккелен', 'Орландо Блум', 'Питер Джексон'], 'reit' : '8.565',
                          'genre' : ['Фэнтези', 'Приключение']})

        self.film2 = Film({'name': 'Крестный отец', 'age': 1972,
                           'actors': ['Марлон Брандо', 'Аль Пачино', 'Марио Пьюзо'], 'reit': '8.739',
                           'genre': ['Драма', 'Криминал']})

        self.film3 = Film({'name': 'Хоббит', 'age': 2012,
                           'actors': ['Иен Маккелен', 'Мартин Фримен', 'Питер Джексон'], 'reit': 8.075,
                           'genre': ['Фэнтези', 'Приключение']})

        self.film4 = Film({'name': 'Шерлок', 'age': '2010',
                           'actors': ['Бенедикт Камбербэтч', 'Матрин Фримен', 'Марк Гейтисс'], 'reit': 8.91,
                           'genre': ['Триллер', 'Драма', 'Криминал']})

        self.film5 = Film({'name': 'Властелин колец: Возвращение Короля', 'age': '2003',
                           'actors': ['Иен Маккелен', 'Орландо Блум', 'Питер Джексон'], 'reit': 8.612,
                           'genre': ['Фэнтези', 'Драма', 'Приключение']})

    def test_init(self):
        self.assertEqual((self.film1.name, self.film1.age, self.film1.actors,
                          self.film1.reit, self.film1.genre),
                         ('Властелин колец: Братство Кольца',2001 ,
                          ['Иен Маккелен', 'Орландо Блум', 'Питер Джексон'], 8.565,
                          ['Фэнтези', 'Приключение']), "Bad")

        self.assertEqual((self.film2.name, self.film2.age, self.film2.actors,
                          self.film2.reit, self.film2.genre),
                         ('Крестный отец', 1972,
                          ['Марлон Брандо', 'Аль Пачино', 'Марио Пьюзо'], 8.739,
                          ['Драма', 'Криминал']), "Bad")

        self.assertEqual((self.film3.name, self.film3.age, self.film3.actors,
                          self.film3.reit, self.film3.genre),
                         ('Хоббит', 2012,
                          ['Иен Маккелен', 'Мартин Фримен', 'Питер Джексон'], 8.075,
                          ['Фэнтези', 'Приключение']), "Bad")

        self.assertEqual((self.film4.name, self.film4.age, self.film4.actors,
                          self.film4.reit, self.film4.genre),
                         ('Шерлок', 2010,
                          ['Бенедикт Камбербэтч', 'Матрин Фримен', 'Марк Гейтисс'], 8.910,
                          ['Триллер', 'Драма', 'Криминал']), "Bad")

        self.assertEqual((self.film5.name, self.film5.age, self.film5.actors,
                          self.film5.reit, self.film5.genre),
                         ('Властелин колец: Возвращение Короля', 2003,
                          ['Иен Маккелен', 'Орландо Блум', 'Питер Джексон'], 8.612,
                          ['Фэнтези', 'Драма', 'Приключение']), "Bad")

film1 = Film({'name' : 'Властелин колец: Братство Кольца', 'age' : '2001',
                           'actors' : ['Иен Маккелен', 'Орландо Блум', 'Питер Джексон'], 'reit' : '8.565',
                          'genre' : ['Фэнтези', 'Приключение']})
film2 = Film({'name': 'Крестный отец', 'age': 1972,
                           'actors': ['Марлон Брандо', 'Аль Пачино', 'Марио Пьюзо'], 'reit': '8.739',
                           'genre': ['Драма', 'Криминал']})
film3 = Film({'name': 'Хоббит', 'age': 2012,
                           'actors': ['Иен Маккелен', 'Мартин Фримен', 'Питер Джексон'], 'reit': 8.075,
                           'genre': ['Фэнтези', 'Приключение']})
film4 = Film({'name': 'Шерлок', 'age': '2010',
                           'actors': ['Бенедикт Камбербэтч', 'Матрин Фримен', 'Марк Гейтисс'], 'reit': 8.91,
                           'genre': ['Триллер', 'Драма', 'Криминал']})
film5 = Film({'name': 'Властелин колец: Возвращение Короля', 'age': '2003',
                           'actors': ['Иен Маккелен', 'Орландо Блум', 'Питер Джексон'], 'reit': 8.612,
                           'genre': ['Фэнтези', 'Драма', 'Приключение']})

class UserTest(unittest.TestCase):
    def setUp(self):
        self.user1 = User('Abramov', '12345')
        self.user2 = User('Borisov', 'qwert')

    def test_init(self):
        self.assertEqual((self.user1.login, self.user1.password, self.user1.queuefilm), ('Abramov', '12345', []))
        self.assertEqual((self.user2.login, self.user2.password, self.user1.queuefilm), ('Borisov', 'qwert', []))

    def test_addfilm(self):
        self.user1.addfilm(film1)
        self.assertEqual(self.user1.queuefilm, [film1])
        self.user1.addfilm(film2, 1)
        self.assertEqual(self.user1.queuefilm, [film2, film1])
        self.user1.addfilm(film3, 3)
        self.assertEqual(self.user1.queuefilm, [film2, film1, film3])
        self.user1.addfilm(film4, 10)
        self.assertEqual(self.user1.queuefilm, [film2, film1, film3, film4])
        self.user1.addfilm(film1, 10)
        self.assertEqual(self.user1.queuefilm, [film2, film1, film3, film4])

    def test_delfilmbyname(self):
        self.user1.addfilm(film1)
        self.user1.addfilm(film2, 1)
        self.user1.addfilm(film3, 3)
        self.user1.addfilm(film4, 10)
        self.user1.delfilmbyname(film3)
        self.assertEqual(self.user1.queuefilm, [film2, film1, film4])
        self.user1.delfilmbyname(film4)
        self.assertEqual(self.user1.queuefilm, [film2, film1])
        self.user1.delfilmbyname(film2)
        self.assertEqual(self.user1.queuefilm, [film1])

    def test_delfilm(self):
        self.user1.addfilm(film1)
        self.user1.addfilm(film2, 1)
        self.user1.addfilm(film3, 3)
        self.user1.addfilm(film4, 10)
        self.user1.delfilm()
        self.assertEqual(self.user1.queuefilm, [film1, film3, film4])
        self.user1.delfilm()
        self.assertEqual(self.user1.queuefilm, [film3, film4])
        self.user1.delfilm()
        self.assertEqual(self.user1.queuefilm, [film4])

    def test_changefilmposition(self):
        self.user1.addfilm(film1)
        self.user1.addfilm(film2, 1)
        self.user1.addfilm(film3, 3)
        self.user1.addfilm(film4, 10)
        self.user1.changefilmposition(film4)
        self.assertEqual(self.user1.queuefilm, [film4, film2, film1, film3])
        self.user1.changefilmposition(film2, 6)
        self.assertEqual(self.user1.queuefilm, [film4, film1, film3, film2])
        self.user1.changefilmposition(film1, 3)
        self.assertEqual(self.user1.queuefilm, [film4, film3, film1, film2])

    def test_sortof(self):
        self.user1.addfilm(film1)
        self.user1.addfilm(film2, 1)
        self.assertEqual(self.user1.sortof('age'), [film2, film1])
        self.user1.addfilm(film3, 3)
        self.assertEqual(self.user1.sortof('reit'), [film2, film1, film3])
        self.user1.addfilm(film4, 10)
        self.user1.addfilm(film5, 2)
        #film2, film5, film1, film3, film4
        self.user1.sortof('age')
        self.assertEqual(self.user1.sortof('age'), [film2, film1, film5, film4, film3])
        self.assertEqual(self.user1.sortof('name'), 'Не удалось отсортировать список фильмов по данному параметру')
        self.assertEqual(self.user1.sortof('reit'), [film4, film2, film5, film1, film3])

    def test_printfilmwithparam(self):
        self.user1.addfilm(film1)
        self.user1.addfilm(film2, 1)
        self.user1.addfilm(film3, 3)
        self.user1.addfilm(film4, 10)
        self.user1.addfilm(film5, 2)
        film2, film5, film1, film3, film4
        self.assertEqual(self.user1.printfilmwithparam('name', 'Властелин'), [ film5, film1])
        self.assertEqual(self.user1.printfilmwithparam('actors', 'Иен Маккелен'), [film5, film1, film3])
        self.assertEqual(self.user1.printfilmwithparam('actors', 'Иен'), [film5, film1, film3])
        self.assertEqual(self.user1.printfilmwithparam('age', 2002), [film5, film3, film4])
        self.assertEqual(self.user1.printfilmwithparam('actors', 'Виктор'), 'Не удалось найти фильмы удовлетворяющие критерию')

if __name__ == '__main__':
    unittest.main()
