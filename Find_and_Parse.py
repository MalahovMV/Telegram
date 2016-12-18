from grab import  Grab
from  bs4 import BeautifulSoup
import random



def get_html(name):
    g  = Grab()
    g.setup(timeout = 30, connect_timeout = 20)
    g.go('http://megogo.net/ru/films/search?q=' +  name)
    return (g.response.body).decode('utf-8')

def parse_film(html):
    soup = BeautifulSoup(html, 'lxml')
    name = list(soup.find_all('a', {'class': 'voi__title-link'}))
    inf = list(soup.find_all('p', {'class': 'voi__info'}))
    film_list=[]
    for i in range(len(name)):
        film_list.append({(str(name[i].text).replace('\n','')).replace('\xa0',' ').strip() + ', ' + str(inf[i])[50:55]:name[i].get('href')})

    return film_list



def parse_find(html):
    g = Grab()
    g.setup(timeout=30, connect_timeout=20)
    g.go(html)
    soup = BeautifulSoup((g.response.body), 'lxml')
    information = soup.find_all('div', {'class' : 'externalRating-item'})
    reload_name = []
    for i in list(information):
        reload_name.append((str(i.text)))
    list_reit= str(reload_name).split(',')
    reit = {}
    reit['IMDb'] = list_reit[1][1:5]
    if reit == ("']"):
        reit['IMDb'] = ' Отсутствует'

    name = str(soup.find('h1', {'class': 'view__title'}).text).replace('\n','').strip().replace('\xa0', ' ')
    actors = str(soup.find_all('ul', {'class' : 'items'})[0].text).replace(' \n\n',', ')
    producers = str(soup.find_all('ul', {'class' : 'items'})[1].text).replace('\n\n','')
    year =soup.find_all('div', {'class' : 'infoi__content'})[1].text
    year=str(year).replace('\n','').replace(' ','')
    genre = soup.find_all('div', {'class' : 'infoi__content'})[3].text
    genre = str(genre).replace(' ','').replace('\n',' ')
    inf_ab_film = {}
    inf_ab_film['name'] = name
    inf_ab_film['genre'] = genre
    inf_ab_film['age'] =year
    act = str(producers) + str(actors).replace('\n','')
    inf_ab_film['actors'] =  act
    inf_ab_film['reit'] = str(reit['IMDb'])[1:]
    return inf_ab_film


def random_choice(genre_v):
    g = Grab()
    g.setup(timeout=30, connect_timeout=20)
    g.go("http://megogo.net/ru/films/"+genre_v)
    soup = BeautifulSoup((g.response.body).decode('utf-8'), 'lxml')
    names=list(soup.find_all('a', {'class': 'voi__title-link'}))
    wrapped =[]
    for name in names:
        match = str(name).split('=')[2]
        link = match.split(' ')[0].strip('\n')[1 : -2]
        wrapped.append(link)

    rand_film = random.randint(0, len(wrapped) - 1)
    return wrapped[rand_film]


def catching_rand_film(genre):
    required_genre = ['genres_arthouse','genres_action','genres_military','genres_detective','genres_adult',
                      'genres_kids','genres_comedy','genres_melodrama','genres_adventures','genres_horror'
                      'genres_thriller','genres_fiction']

    if genre == 'arthouse':
        return random_choice('genres_arthouse')
    elif genre == 'action':
        return random_choice('genres_action')
    elif genre == 'military':
        return random_choice('genres_military')
    elif genre == 'detective':
        return random_choice('genres_detective')
    elif genre == 'adult':
        return random_choice('genres_adult')
    elif genre == 'kids':
        return random_choice('genres_kids')
    elif genre == 'comedy':
        return random_choice('genres_comedy')
    elif genre == 'melodrama':
        return random_choice('genres_melodrama')
    elif genre == 'adventures':
        return random_choice('genres_adventures')
    elif genre == 'horror':
        return random_choice('genres_horror')
    elif genre == 'thriller':
        return random_choice('genres_thriller')
    elif genre == 'fiction':
        return random_choice('genres_fiction')
    elif genre == 'any':
        random.shuffle(required_genre)
        return random_choice(required_genre[0])
