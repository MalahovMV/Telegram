import requests
from bs4 import BeautifulSoup

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
    for i in range(1,7):
        link = inf[i][9:inf[i].index('>') - 1]
        name = inf[i][inf[i].index('>') + 1 : inf[i].index(',') + 6]
        film_and_link[name] = link

    return(film_and_link)

def get_name(name):
    namebegin = name.index('<b>') + 3
    nameend = name.index('</b>')
    return name[namebegin:nameend]

def get_age(inform):
    ind = inform.index(')')
    inform = inform[ind:].split(' ')
    return inform[3][:4]

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
    film1 = {'name': get_name(name), 'age': get_age(inf[2]),
                  'actors': get_actors(inf[2]), 'reit': get_reit(inf[3]),
                  'genre': get_genre(inf[1])}


    print(film1)

if __name__ == '__main__':
    name = input('film - ')
    film = get_list_film(parse_find(get_html('https://m.kinopoisk.ru?search=%s' % name)))
    print(film.keys())
    real_name = input('Выберите из найденного списка нужный вам фильм')
    inf, name = parse_film(get_html(film[real_name]))
    createdict(inf, name)