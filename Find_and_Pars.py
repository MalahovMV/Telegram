import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text.encode('cp1251')

def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    information = soup.find('div', {'class' : 'block film'})
    name = soup.find('p', {'class' : 'title'})
    return str(information), str(name)

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
    return inf[3][ind + 2: ind + 6]

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
    for i in range(320, 500):
        inf, name = parse(get_html('https://m.kinopoisk.ru/movie/%s/' % str(i)))
        createdict(inf, name)
