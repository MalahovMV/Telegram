import requests
import copy
from bs4 import BeautifulSoup
from peewee import*
from ptwee_db_orm import add_film,print_films,is_checked,len_db,del_film

def get_html(url):
    response = requests.get(url)
    return response.text.encode('cp1251')

def parse_film(html):
    soup = BeautifulSoup(html, 'lxml')
    information = soup.find('div', {'class' : 'block film'})
    name = soup.find('p', {'class' : 'title'})
    return str(information), str(name)

def parse_find(html):
    soup = BeautifulSoup(html, 'lxml')
    information = soup.find('div', {'id' : 'content'})
    return str(information)

def get_list_film(inf):
    inf = inf.split('<span>')
    film_and_link = {}
    i = 1
    while i > 0:
        try:
            link = inf[i][9:inf[i].index('>') - 1]
            name = inf[i][inf[i].index('>') + 1 : inf[i].index(',') + 6]
            film_and_link[name] = link
            i += 1

        except:
            i = 0

    return(film_and_link)

def get_name(name):
    namebegin = name.index('<b>') + 3
    nameend = name.index('</b>')
    return name[namebegin:nameend]

def get_age(name):
    agebegin = name.index('<span>')
    ageend = name.index('</span>')
    age = name[agebegin : ageend].split(', ')
    try:
        return age[-2][-4:]

    except:
        return age[0][-4:]

def get_actors(inform):
    actors = []
    inform = inform.split('</a>')
    for s in inform:
        i = len(s) - 1
        while s[i] != '>':
            i -= 1

        actors.append(s[i + 1:])

    return actors[:-2]

def get_reit(inform):
    ind = inform.index('i')
    return inform[ind + 2: ind + 6]

def get_genre(inform):
    inform = inform[:len(inform) - 8]
    return inform.split(', ')

def createdict(inf, name):
    inf = inf.split('<span>')
    film1 = {'name': get_name(name), 'age': get_age(name),
                  'actors': get_actors(inf[2]), 'reit': get_reit(inf[3]),
                  'genre': get_genre(inf[1])}

    if is_checked():  # кажется, что в обоих случаях одинаково работает прост add, но внутри is_checked  еще делает действие,
        #  а последний шаг одинаковый
        add_film(str(film1['name']), len_db(), str(film1['age']), str(film1['actors']), str(film1['reit']),
                 str(film1['genre']))
    else:
        add_film(str(film1['name']), len_db(), str(film1['age']), str(film1['actors']), str(film1['reit']),
                 str(film1['genre']))

def main_pars():
    name = input('film - ')
    film = get_list_film(parse_find(get_html('https://m.kinopoisk.ru?search=%s' % name)))
    if len(film) == 0:
        print('Нет фильмов с таким или похожим названием')

    else:
        i = 1
        for key in sorted(film.keys()):
            print(str(i), key)
            i += 1

        real_name = input('Выберите из найденного списка нужный вам фильм по номеру ')
        inf, name = parse_film(get_html(film[sorted(film.keys())[int(real_name) - 1]]))
        createdict(inf, name)
        print_films()

if __name__ == '__main__':
    main_pars()