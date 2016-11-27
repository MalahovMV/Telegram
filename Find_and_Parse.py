from grab import  Grab
import datetime
from  bs4 import BeautifulSoup



def get_html(name):
    g  = Grab()
    g.setup(timeout = 30, connect_timeout = 20)
    resp = g.go('http://megogo.net/ru/films/search?q=' +  name)
    return (g.response.body).decode('utf-8')

def parse_film(html):
    soup = BeautifulSoup(html, 'lxml')
    name = list(soup.find_all('a', {'class': 'voi__title-link'}))
    inf = list(soup.find_all('p', {'class': 'voi__info'}))
    film_list=[]
    for i in range(len(name)):
        film_list.append({(str(name[i].text).replace('\n','')).replace('\xa0',' ').strip() + ', ' + str(inf[i])[50:55]:name[i].get('href')})

    if len(film_list) > 10:
        return ('Уточните запрос, пожалуйста')

    return film_list



def parse_find(html):
    g = Grab()
    g.setup(timeout=30, connect_timeout=20)
    resp = g.go(html)
    soup = BeautifulSoup((g.response.body), 'lxml')
    information = soup.find_all('div', {'class' : 'externalRating-item'})
    reload_name = []
    for i in list(information):
        reload_name.append((str(i.text)))
    list_reit= str(reload_name).split(',')
    reit = {}
    #reit['Кинопоиск']=list_reit[0][1:5]
    reit['IMDb'] = list_reit[1][1:5]
    name = str(soup.find('h1', {'class': 'view__title'}).text).replace('\n','').strip().replace('\xa0', ' ')
    #plot=str(soup.find('div', {'class' : 'full full-preload storyLazyLoad'}).text).replace('\xa0',' ')
    actors = str(soup.find_all('ul', {'class' : 'items'})[0].text).replace(' \n\n',', ')
    producers = str(soup.find_all('ul', {'class' : 'items'})[1].text).replace('\n\n','')
    year =soup.find_all('div', {'class' : 'infoi__content'})[1].text
    year=str(year).replace('\n','').replace(' ','')
   # country=soup.find_all('div', {'class' : 'infoi__content'})[2].text
    #country=str(country).replace(' ','').replace('\n','')
    genre = soup.find_all('div', {'class' : 'infoi__content'})[3].text
    genre = str(genre).replace(' ','').replace('\n',' ')
    #time = soup.find_all('div', {'class' : 'infoi__content'})[4].text
    #time =str(time).replace(' ','').replace('\n','')
    #subtitles =soup.find_all('div', {'class' : 'infoi__content'})[8].text
    #subtitles_reload = str(subtitles).replace(' ','').replace('\n','')
    #permissible_age=subtitles =soup.find_all('div', {'class' : 'infoi__content'})[5].text
    #permissible_age =str(permissible_age).replace(' ','').replace('\n','')
    inf_ab_film = {}
    inf_ab_film['name'] = name
    inf_ab_film['genre'] = genre
    inf_ab_film['age'] =year
    #inf_ab_film['Страна'] = country
    #inf_ab_film['Рейтинг'] = 'Кинопоиск -'+ str(reit['Кинопоиск'])+ ' '+'IMDb -'+str(reit['IMDb'])
    #inf_ab_film['Допустимый возраст'] =permissible_age
    #inf_ab_film['Субтитры'] = subtitles_reload
    #inf_ab_film['Длительность'] =time
    #inf_ab_film['Описание'] = str(plot)
    act = str(producers) + str(actors).replace('\n','')
    inf_ab_film['actors'] =  act
    #inf_ab_film['Режиссура'] = producers
    inf_ab_film['reit'] = str(reit['IMDb'])[1:]
    return inf_ab_film


#p=datetime.datetime.now().second
#for i in range (100):
#    current_time = datetime.datetime.now().second-p
#    if current_time < 0:
#        current_time+=60
#        print ('{0},{1}'.format(i,current_time))
#    else:
#        print('{0},{1}'.format(i,current_time))
#    get_html()
if __name__ == '__main__':
    name = input('film- ' )
    some_f=(parse_film(get_html(name)))
    print(some_f)
    number = int(input('Nomer- '))
    print(parse_find((str(some_f[number].values())[14:-3])))
    #print(parse_find('http://megogo.net/ru/view/28549-titanik.html'))
